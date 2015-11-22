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

import requests
from core.models import InnleveringUser, UserVote, Bidrag


def user_has_group(user, groupName):
    # Determine if a user is in a group
    if user.groups.filter(name=groupName).count():
        return True

    return False


def user_is_crew(user):
    return user_has_group(user, "Crew")


def has_voted(user, bidrag):
    # Has voted in compo?
    voted = UserVote.objects.filter(user=user)

    if voted.count() > 0:
        for vote in voted:
            thisvoted = Bidrag.objects.filter(id=vote.bidrag.id)
            if thisvoted.count() > 0:
                return True

        return True

    return False


def get_innlevering_user(user):
    inn = InnleveringUser.objects.filter(user=user)
    if inn.count() > 0:
        return inn[0]


# Determine if a user can upload a bidrag.
def can_upload(user):
    return user_is_crew(user) or ge_has_valid_ticket(user)


def ge_has_valid_ticket(user):
    # Fetch the innlevering user of this one.
    # innleveringuser = get_innlevering_user(user)

    # if innleveringuser:
    #	data = {
    #		"user_id": innleveringuser.geID,
    #		"token": innleveringuser.currenttoken,
    #		"timestamp": innleveringuser.currenttimestamp,
    #		"eventID": 82
    #	}

    #	result = requests.post("https://www.geekevents.org/sso/user-has-tickets/", params=data)

    #	numberOfTickets = 0

    #	try:
    #		numberOfTickets = int(result.text)
    #	except ValueError:
    #		return False

    # Validate number of tickets
    #	if numberOfTickets > 0:
    #		return True

    return True
