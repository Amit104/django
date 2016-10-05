from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    score = models.CharField(max_length=25, blank=True)

class CategoriesQ(models.Model):
	Name = models.CharField(max_length=255)
	Noq = models.IntegerField(default = 0)
	Cid = models.AutoField(primary_key=True)

	def __str__(self):
		return self.Name

class Questions(models.Model):
	Name = models.CharField(max_length=25)
	Statement = models.FileField()
	Difficulty = models.CharField(max_length=10)
	Memory_limit = models.IntegerField()
	Time_limit = models.IntegerField()

	def __str__(self):
		return self.Name


class Testcase(models.Model):
	inputTestFile = models.FileField()
	outputTestFile = models.FileField()
	Qid = models.ForeignKey(Questions)

class Submission(models.Model):
	time_taken = models.IntegerField()
	time_limit = models.IntegerField()
	language = models.CharField(max_length=5)
	score = models.CharField(max_length=25, blank=True)
	Qid = models.ForeignKey(Questions)
	Uid = models.ForeignKey(UserProfile)

class Ins(models.Model):
	questions = models.ForeignKey(Questions)
	category = models.ForeignKey(CategoriesQ)