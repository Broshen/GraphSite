from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import GraphJob, AdjacencyListFile
import subprocess

@shared_task
def run_exe(pk):
    job = GraphJob.objects.get(pk=pk)
    job.status = "Running"
    job.save()

    p = subprocess.Popen('./media/executables/GraphProfile.exe',
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        encoding='ascii')

    p.communicate(input=job.job_input)

    job.status = "Finished"
    job.save()
    return

