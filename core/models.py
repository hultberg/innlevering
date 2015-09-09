from django.db import models
import time
import os
from django.contrib.auth.models import User


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

    # Provides all bidrags for this compo.
    def get_bidrag(self):
        return Bidrag.objects.filter(compo=self.id)


class Bidrag(models.Model):
    name = models.CharField(max_length=120)
    data = models.TextField()
    created = models.DateTimeField(auto_now=True)
    compo = models.ForeignKey("Compo")
    creator = models.ForeignKey(User, unique=True)
    votes = models.IntegerField()

    #
    def __str__(self):
        return self.name

    # Provides all files for this compo.
    def get_files(self):
        return BidragFile.objects.filter(bidrag=self)

    # Provides number of files for this compo.
    def get_num_files(self):
        return self.get_files().count()

    @property
    def get_thebidrag_file(self):
        if self.get_num_files() > 0:
            return self.get_files()[0]


class BidragFile(models.Model):
    bidrag = models.ForeignKey("Bidrag")
    file = models.FileField(upload_to=update_filename)
    time = models.DateTimeField(auto_now=True)

    #
    def __str__(self):
        return self.bidrag.name + "_fil" + str(self.id)