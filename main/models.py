from django.db import models
from django.db.models.aggregates import Max

class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()

    a = models.CharField(max_length=50)
    a_right = models.BooleanField()

    b = models.CharField(max_length=50)
    b_right = models.BooleanField()

    c = models.CharField(max_length=50)
    c_right = models.BooleanField()

    d = models.CharField(max_length=50)
    d_right = models.BooleanField()

    def __str__(self):
        return self.title


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    thumb = models.ImageField()

    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name


class UserForm(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    years = models.IntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " " + self.surname


class ProposeForm(models.Model):
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title