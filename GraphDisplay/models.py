from django.db import models

# Create your models here.
class GraphJob(models.Model):
	name = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default="Not Running")
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	metrics = models.TextField() # stores the metrics JSON from the form
	job_input = models.TextField() # actual input to feed into GraphProfile 
	graph_file = models.ManyToManyField('AdjacencyListFile')

class AdjacencyListFile(models.Model):
	file_name = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	file = models.FileField(upload_to='uploads/')

	def __str__ (self):
		return self.file_name

# class ExperimentMetrics(models.Model):
# 	abc - 1 entry (vertex) - outputs number
# 	adiam - no entries - outputs number
# 	aprank - no entries - list of numbers
# 	bbc - no entries - list of numbers
# 	bc - no entries - list of numbers
# 	cc - no entries - 2 numbers - Connected Components, Largest Component Sizes: 
# 	dist - 2 entries (verticies) - outputs number
# 	ediam - no entries - outputs number
# 	emdiam - no entries - outputs number
# 	edge - no entries - outputs number
# 	etri - no entries - outputs number
# 	kdiam - no entries - 2 numbers (lower, upper bounds)
# 	lcc - 1 entry (vertex) - outputs number
# 	od - no entries - number + list of numbers
# 	prank - no entries - list of numbers
# 	vert - no entries - outputs number
# 	reduce - 1 entry (# of verticies to keep) - outputs adjaceny list
#	reducetree - user can enter as many as they want - outputs adjaceny list
#	reducetreetop - 1 entry (# of vertices as roots) - outputs adjaceny list
#	reducetri - 1 entry (# of edges to keep for each vertex) - outputs adjaceny list
#	reducepercent - 1 entry (% of edges to keep for each vertex) - outputs adjaceny list


# class ExperimentResults(models.Model):
