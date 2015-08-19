from django.db import models
import time
import os


def update_filename(instance, filename):
    path = "bidrag/" + time.strftime('%d-%Y') + "/"
    format = filename
    return os.path.join(path, format)


# Create your models here.
class Compo(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    htmlContent = models.TextField(default="")

    #
    def __str__(self):
        return self.name


class Bidrag(models.Model):
    name = models.CharField(max_length=120)
    data = models.TextField()
    fileLocation = models.CharField(max_length=230)
    created = models.DateTimeField(auto_now=True)
    compo = models.ForeignKey("Compo")
    file = models.FileField(upload_to=update_filename)
    votes = models.IntegerField()

    #
    def __str__(self):
        return self.name
