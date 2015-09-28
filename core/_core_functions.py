import requests

def user_has_group(user, groupName):
    # Determine if a user is in a group
    if user.groups.filter(name=groupName).count():
        return True

    return False


def user_is_crew(user):
    return user_has_group(user, "Crew")


def get_innlevering_user(user):
	inn = InnleveringUser.objects.filter(user=user)
	if inn.count() > 0:
		return inn[0]


# Determine if a user can vote on bidrags.
def can_vote(user):
	return user_is_crew(user) or ge_has_valid_ticket(user)


# Determine if a user can upload a bidrag.
def can_upload(user):
	return user_is_crew(user) or ge_has_valid_ticket(user)


def ge_has_valid_ticket(user):
	# Fetch the innlevering user of this one.
	innleveringuser = get_innlevering_user(user)
	
	data = {
		"user_id": innleveringuser.geID,
		"token": innleveringuser.currenttoken,
		"timestamp": innleveringuser.currenttimestamp,
		"eventID": 82
	}

	result = requests.post("https://www.geekevents.org/sso/user-has-tickets/", params=data)

	numberOfTickets = 0

	try:
		numberOfTickets = int(result.text())
	except ValueError:
		return False

	# Validate number of tickets
	if numberOfTickets > 0:
		return True

	return False
