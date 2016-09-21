from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    score = models.CharField(max_length=250, blank=True)

class Testcase(models.Model):
	testfile = models.FileField()

class Questions(models.Model):
	Name = models.CharField(max_length=25)
	Statement = models.CharField(max_length=250)
	Difficulty = models.CharField(max_length=2)
	Input_Format = models.CharField(max_length=50)
	Input_Constraints = models.CharField(max_length=50)
	Input_Sample = models.CharField(max_length=50)
	Ouput_Format = models.CharField(max_length=50)
	Ouput_Constraints = models.CharField(max_length=50)
	Ouput_Sample = models.CharField(max_length=50)
	Memory_limit = models.IntegerField()
	Time_limit = models.IntegerField()
	Tid = models.ForeignKey(Testcase)

class Submission(models.Model):
	time_taken = models.IntegerField()
	time_limit = models.IntegerField()
	language = models.CharField(max_length=5)
	score = models.IntegerField()
	Qid = models.ForeignKey(Questions)
	Uid = models.ForeignKey(UserProfile)

class CategoriesQ(models.Model):
	Name = models.CharField(max_length=255)
	Noq = models.IntegerField(default = 0)
	Cid = models.AutoField(primary_key=True)

	def __str__(self):
		return self.Name

class Ins(models.Model):
	questions = models.ForeignKey(Questions)
	category = models.ForeignKey(CategoriesQ)