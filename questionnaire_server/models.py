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

    def __unicode__(self):
        return self.answer

