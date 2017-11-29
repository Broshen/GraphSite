from __future__ import absolute_import, unicode_literals
from django.core.files import File
from django.conf import settings
from celery import shared_task
from .models import GraphJob, AdjacencyListFile, ResultFile
from .constants import output_file_globs
import subprocess
import glob, os

@shared_task
def run_exe(pk):
    job = GraphJob.objects.get(pk=pk)
    job.status = "Running"
    job.save()
    try:
        p = subprocess.Popen('./media/executables/GraphProfile.exe',
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='ascii')

        p.communicate(input=job.job_input)
    except PermissionError:
        os.chmod('./media/executables/GraphProfile.exe', 0o777)
        p = subprocess.Popen('./media/executables/GraphProfile.exe',
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='ascii')

        p.communicate(input=job.job_input)

    resultFilePks = []

    for file_glob in output_file_globs:
        output_files = glob.iglob(file_glob)
        for output_file in output_files:
            # copy the output file into a resultfile object
            result = ResultFile()
            result.file = File(open(output_file))
            # rename the path to get rid of the /media/upload
            # new file is placed in the /media/results folder
            filename = result.file.name.split("\\")[-1]
            result.file.name = filename
            result.save()

            # delete the original file afterwards
            if os.path.exists(output_file):
                os.remove(output_file)

            # add pks to be linked to the job object later
            resultFilePks.append(result.pk)

    # delete old result files
    job.results.all().delete()

    # link new result files
    job.results = (resultFilePks)

    job.status = "Finished"
    job.save()
    return

