from django.contrib.auth.models import User
from django.db import models

class MultipleChoiceAnswer(models.Model):
    text = models.CharField(max_length=500)

    def __unicode__(self):
        return self.text


class Question(models.Model):
    question = models.CharField(max_length=500)
    is_multiple_choice = models.BooleanField(default=False)
    multiple_choice_answer = models.ManyToManyField(MultipleChoiceAnswer, blank=True)
    survey = models.ForeignKey('Survey', blank=True)

    def __unicode__(self):
        return self.question


class Survey(models.Model):
    study = models.ForeignKey('Study')


class UserAnswer(models.Model):
    answer = models.CharField(max_length=500)
    question = models.ForeignKey(Question)
    patient = models.ForeignKey('Patient')

    def __unicode__(self):
        return self.answer


class Study(models.Model):
    name = models.CharField(max_length=500)
    creator = models.ForeignKey(User, related_name="created_studies")
    administrators = models.ManyToManyField(User)
    participants = models.ManyToManyField('Patient', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name



class Patient(models.Model):
    patient_id = models.CharField(max_length=100, primary_key=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.patient_id

