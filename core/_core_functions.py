

def user_has_group(user, groupName):
    # Determine if a user is in a group
    if user.groups.filter(name=groupName).count():
        return True

    return False


def user_is_crew(user):
    return user_has_group(user, "Crew")


def get_innlevering_user(user):
	inn = InnleveringUser.objects.filter(user=user)
	if inn.count() < 1:
		return -1

	return inn[0]


def ge_has_valid_ticket(user):
	# Fetch the innlevering user of this one.
	innleveringuser = get_innlevering_user(user)
	if 

	return ""
