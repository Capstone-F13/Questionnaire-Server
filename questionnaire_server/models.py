from django.db import models

class MultipleChoiceAnswer(models.Model):
    text = models.CharField(max_length=500)

    def __unicode__(self):
        return self.text


class Question(models.Model):
    question = models.CharField(max_length=500)
    is_multiple_choice = models.BooleanField(default=False)
    multiple_choice_answer = models.ManyToManyField(MultipleChoiceAnswer, blank=True)

    def __unicode__(self):
        return self.question


class UserAnswer(models.Model):
    answer = models.CharField(max_length=500)
    question = models.ForeignKey(Question)
    patient = models.ForeignKey('Patient')

    def __unicode__(self):
        return self.answer

class Patient(models.Model):
    patient_ID = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
	
