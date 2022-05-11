def roles_string_to_roles_list(roles_string):
    roles_list = roles_string.split(",")
    if roles_list[-1] == "":
        roles_list.pop(-1)

    return roles_list
