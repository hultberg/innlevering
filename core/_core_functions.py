import requests
from core.models import InnleveringUser, UserVote, Bidrag

def user_has_group(user, groupName):
    # Determine if a user is in a group
    if user.groups.filter(name=groupName).count():
        return True

    return False


def user_is_crew(user):
    return user_has_group(user, "Crew")


def has_voted(user, bidrag, compo):
    vote = UserVote.objects.filter(user=user, bidrag=bidrag)

    if vote.count() > 0:
    	return True

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
	#innleveringuser = get_innlevering_user(user)

	#if innleveringuser:	
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
