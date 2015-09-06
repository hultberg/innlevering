

def user_has_group(user, groupName):
    # Determine if a user is in a group
    if user.groups.filter(name=groupName).count():
        return True

    return False


def user_is_crew(user):
    return user_has_group(user, "Crew")
