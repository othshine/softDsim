def addRolesToUser(user, roles):

    if not roles:
        return user

    if "superuser" in roles:
        user.is_superuser = True

    if "staff" in roles:
        user.is_staff = True

    return user
