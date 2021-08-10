from django.db import models
from account.models import User
from ckeditor.fields import RichTextField


class Question(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    body                    = RichTextField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    total_answers           = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    question                = models.ForeignKey(Question, on_delete=models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    body                    = RichTextField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    in_reply_to             = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    # upvotes                 = models.IntegerField(default=0)
    # downvotes               = models.IntegerField(default=0)
    chosen                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Vote(models.Model):
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    answer                = models.ForeignKey(Answer, on_delete=models.CASCADE)
    create_date           = models.DateTimeField(auto_now_add=True)
    update_date           = models.DateTimeField(auto_now=True)
    up                    = models.BooleanField(default=False)
    down                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'