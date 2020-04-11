from django.contrib.auth.models import User
from django.db import models


# Само голосование
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    liked = models.IntegerField(default=0)
    allow_many_answers = models.BooleanField(default=0)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()


# Вариант ответа на голосование
class VoteVariant(models.Model):
    vote = models.ForeignKey(to=Vote, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)


# Выбор, сделанный пользователем
class UserVote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vote = models.ForeignKey(to=Vote, on_delete=models.CASCADE)
    vote_variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class UserLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vote = models.ForeignKey(to=Vote, on_delete=models.CASCADE)
    created_at = models.DateTimeField()