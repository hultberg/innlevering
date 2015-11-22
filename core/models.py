"""
  Copyright 2015 Edvin Hultberg

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from django.db import models
import time
import os
from django.contrib.auth.models import User
from django.conf import settings


def update_filename(instance, filename):
    path = "bidrag/" + time.strftime('%d-%Y') + "/"
    format = filename
    return os.path.join(path, format)


# Create your models here.
class InnleveringUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    geID = models.IntegerField()
    geUsername = models.TextField(default="")
    currenttoken = models.TextField(default="")
    currenttimestamp = models.TextField(default="")

    #
    def __str__(self):
        return self.geUsername


# Create your models here.
class Compo(models.Model):
    name         = models.CharField(max_length=120)
    description  = models.TextField()
    htmlContent  = models.TextField(default="")
    isPublished  = models.BooleanField(default=False)
    isVotingMode = models.BooleanField(default=False)

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
    creator = models.ForeignKey(User, unique=False)
    votes = models.IntegerField()

    class Meta:
        unique_together = ('compo', 'creator',)

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
    def creator_name(self):
        return self.creator.username

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


class UserVote(models.Model):
    bidrag = models.ForeignKey("Bidrag")
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('bidrag', 'user',)

    #
    def __str__(self):
        return self.user.username + " vote on bID: " + str(self.bidrag.id)
