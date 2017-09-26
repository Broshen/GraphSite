from __future__ import absolute_import, unicode_literals
from django.core.files import File
from django.conf import settings
from celery import shared_task
from .models import GraphJob, AdjacencyListFile, ResultFile
import subprocess
import glob, os

output_file_globs = [
    "./media/uploads/*-graph-properties.txt",
    "./media/uploads/*-page-rank.txt",
    "./media/uploads/*-approximate-page-rank.txt",
    "./media/uploads/*-betweenness-centrality.txt",
    "./media/uploads/*-brandes-BC.txt",
    "./media/uploads/*-reduced-graph.txt",
    "./media/uploads/*-reduced-graph5.txt",
    "./media/uploads/*-reduced-graph5.txt",
    "./media/uploads/*-reduced-graph Tree.txt",
    "./media/uploads/*-reduced-graph-tree2.txt",
    "./media/uploads/*-reduced-graph-triangle.txt",
    "./media/uploads/*-reduced-graph-proportion.txt",
]

@shared_task
def run_exe(pk):
    job = GraphJob.objects.get(pk=pk)
    job.status = "Running"
    job.save()
    print("A")
    try:
        print("B")
        p = subprocess.Popen('./media/executables/GraphProfile.exe',
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='ascii')

        p.communicate(input=job.job_input)
    except PermissionError:
        print("C")
        os.chmod('./media/executables/GraphProfile.exe', 0o777)
        p = subprocess.Popen('./media/executables/GraphProfile.exe',
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='ascii')

        p.communicate(input=job.job_input)

    resultFilePks = []
    print("D")

    for file_glob in output_file_globs:
        output_files = glob.iglob(file_glob)
        print("E")
        for output_file in output_files:
            print("F")
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
            print("G")

    # delete old result files
    job.results.all().delete()

    # link new result files
    job.results = (resultFilePks)

    job.status = "Finished"
    job.save()
    return

