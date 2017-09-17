from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django import forms
from .models import GraphJob, AdjacencyListFile
from .forms import ALFileForm
import subprocess
import json

def run_exe(request):
	# inputfile = open('./GraphDisplay/static/test_commands/test0.in')
	# #print(inputfile.read())
	# p = subprocess.Popen('./GraphDisplay/static/GraphProfile.exe', stdin=inputfile)
	# inputfile.close()
	return HttpResponseRedirect(reverse("GraphDisplay:tasks"))

def view_tasks(request):
	# outputfile = open('./Graph Properties.txt')
	# output = outputfile.read()
	# outputfile.close()
	return HttpResponse(output)


# interface to run graph jobs
class GraphJobInterface():
	# takes a string representing the JSON object 
	# and outputs a list of commands to pipe into the executable
	@staticmethod
	def create_commands(metrics_string, files):
		metrics_JSON = json.loads(metrics_string)

		commands = ""
		
		for file in files:
			commands += file +"\n"

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
		return commands

class GraphJobCreateView(CreateView, GraphJobInterface):
	model = GraphJob
	fields = ['name', 'metrics', 'graph_file',]
	template_name = "GraphDisplay/graph_job_form.html"
	success_url = reverse_lazy("GraphDisplay:dashboard")

	def post(self, request, *args, **kwargs):
		super(GraphJobCreateView, self).post(request, *args, **kwargs)
		self.object.job_input = self.create_commands(
										self.object.metrics,
										self.object.graph_file.values_list('file', flat=True))
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())

		

class GraphJobManageView(TemplateView):
	template_name = "GraphDisplay/dashboard.html"
	fields = ['name', 'metrics', 'graph_file',]

	def get_context_data(self, **kwargs):
		context = super(GraphJobManageView, self).get_context_data(**kwargs)
		context["graph_jobs"] = GraphJob.objects.all().order_by('-last_modified')
		return context

class GraphJobUpdateView(UpdateView, GraphJobInterface):
	model = GraphJob
	fields = ['name', 'metrics', 'graph_file',]
	success_url = reverse_lazy("GraphDisplay:dashboard")
	template_name = "GraphDisplay/graph_job_form.html"


	def post(self, request, *args, **kwargs):
		super(GraphJobUpdateView, self).post(request, *args, **kwargs)
		self.object.job_input = self.create_commands(
										self.object.metrics,
										self.object.graph_file.values_list('file', flat=True))
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())

class GraphJobDetailView(DetailView):
	model = GraphJob
	template_name = "GraphDisplay/graph_job_view.html"


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