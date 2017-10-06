from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django import forms
from .models import GraphJob, AdjacencyListFile, ResultFile
from .forms import ALFileForm
from .tasks import run_exe
from celery import uuid
from celery.task.control import revoke
import json

# interface to run graph jobs
class GraphJobInterface():
    # takes a string representing the JSON object 
    # and outputs a list of commands to pipe into the executable
    def create_commands(self):
        metrics_JSON = json.loads(self.object.metrics)

        commands = ""
        
        for gf_obj in self.object.graph_file.all():
            commands += "." + gf_obj.file.url +"\n"
            for key, val in metrics_JSON.items():
                commands += key+"\n"
                if(isinstance(val, str)):
                    commands += val + "\n"
                elif(key == "dist"):
                    commands += val[0] + "\n"
                    commands += val[1] + "\n"
                elif(key == "reducetree"):
                    for v in val:
                        commands += v + "\n"
                    commands += "-1\n"

            commands += "exit\n"
            
        commands += "exit\n"

        self.object.job_input = commands
        self.object.save()

    def toggle_job(self):
        # if task is currently running, get id and stop it
        if(self.object.status == "Running" or self.object.status == "Queued"):
            revoke(self.object.celery_task_id, terminate=True)
            self.object.status = "Stopped"
            self.object.save()
        else: # otherwise, queue the task
            self.object.status = "Queued"
            self.object.celery_task_id = uuid()
            self.object.save()
            run_exe.apply_async(args=[self.object.pk], task_id=self.object.celery_task_id)

class GraphJobCreateView(CreateView, GraphJobInterface):
    model = GraphJob
    fields = ['name', 'metrics', 'graph_file',]
    template_name = "GraphDisplay/graph_job_form.html"

    def post(self, request, *args, **kwargs):
        super(GraphJobCreateView, self).post(request, *args, **kwargs)
        self.create_commands()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('GraphDisplay:job_view',kwargs={'pk':self.object.id,})

    def get_context_data(self, **kwargs):
        context = super(GraphJobCreateView, self).get_context_data(**kwargs)
        return context

class GraphJobManageView(TemplateView):
    template_name = "GraphDisplay/dashboard.html"
    fields = ['name', 'metrics', 'graph_file',]

    def get(self, request, *args, **kwargs):
        return super(GraphJobManageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GraphJobManageView, self).get_context_data(**kwargs)
        context["graph_jobs"] = GraphJob.objects.all().order_by('-last_modified')
        return context

class GraphJobUpdateView(UpdateView, GraphJobInterface):
    model = GraphJob
    fields = ['name', 'metrics', 'graph_file',]
    template_name = "GraphDisplay/graph_job_form.html"

    def post(self, request, *args, **kwargs):
        super(GraphJobUpdateView, self).post(request, *args, **kwargs)
        self.create_commands()
        return HttpResponseRedirect(reverse("GraphDisplay:job_view", kwargs=kwargs))

    def get_success_url(self):
        return reverse('GraphDisplay:job_view',kwargs={'pk':self.object.id,})

class GraphJobDetailView(DetailView, GraphJobInterface):
    model = GraphJob
    template_name = "GraphDisplay/graph_job_view.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.toggle_job()
        return HttpResponseRedirect(reverse("GraphDisplay:job_view", kwargs=kwargs))

    def get_context_data(self, **kwargs):
        context = super(GraphJobDetailView, self).get_context_data(**kwargs)
        if(self.object.status == "Not Running" or self.object.status == "Finished" or self.object.status == "Stopped"):
            context["action"] = "Start"
        else:
            context["action"] = "Stop"
        return context

class GraphJobDeleteView(DeleteView):
    model = GraphJob
    success_url = reverse_lazy("GraphDisplay:dashboard")















# this view allows users to upload adjaceny list files
class ALFileCreateView(FormView):
    form_class = ALFileForm
    success_url = reverse_lazy("GraphDisplay:graphs")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                AdjacencyListFile(file_name=f.name, file=f).save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ALFileManageView(TemplateView):
    template_name = "GraphDisplay/adjacency_list_file_manage.html"

    def get(self, request, *args, **kwargs):
        return super(ALFileManageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ALFileManageView, self).get_context_data(**kwargs)
        context['upload_url'] = reverse("GraphDisplay:graph_new")
        context['files'] = AdjacencyListFile.objects.all().order_by('-last_modified')
        return context

class ALFileUpdateView(UpdateView):
    model = AdjacencyListFile
    fields = ['file']
    success_url = reverse_lazy("GraphDisplay:graphs")

    def post(self, request, *args, **kwargs):
        super(ALFileUpdateView, self).post(request, *args, **kwargs)
        new_file =  request.FILES.getlist('file_field')[0]

        # delete old file
        self.object.file.delete()

        # assign new uploaded file and update the name
        self.object.file = new_file
        self.object.file_name = new_file.name

        # save changes
        self.object.save()
        return HttpResponseRedirect(reverse("GraphDisplay:graphs"))

class ALFileDeleteView(DeleteView):
    model = AdjacencyListFile
    success_url = reverse_lazy("GraphDisplay:graphs")

    def post(self, request, *args, **kwargs):
        super(ALFileDeleteView, self).post(request, *args, **kwargs)
        # delete associated file
        self.object.file.delete()

        self.object.delete()
        return HttpResponseRedirect(reverse("GraphDisplay:graphs"))