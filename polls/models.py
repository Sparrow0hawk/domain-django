from django.db import models


class QuestionEntity(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=200)


class ChoiceEntity(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(QuestionEntity, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
