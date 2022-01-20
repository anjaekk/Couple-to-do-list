from django.db import models
from django.urls import reverse

from core.models import TimestampedModel
from users.models import User


THEME = (
    (0, "restaurant"),
    (1, "place"),
    (2, "museum")
)

class Task(TimestampedModel):
    theme = models.SmallIntegerField(choices=THEME)
    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=500)
    place = models.CharField(max_length=200)
    note = models.TextField()
    is_done = models.BooleanField(default=False)
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk':self.pk})