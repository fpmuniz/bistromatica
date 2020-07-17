from django.db import models


class ThreadItem(models.Model):
	post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
	thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
	position = models.IntegerField(null=True)
