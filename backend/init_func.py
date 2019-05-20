def init_permission(auths):
    permissions_dict = {}
    for auth in auths:
        if not permissions_dict.get(auth["role_id"]):
            permissions_dict[auth["role_id"]] = {
                "url": [auth["auth__permission_url"]],
                "action": [auth["auth__act"]]
            }
        else:
            permissions_dict[auth["role_id"]]["url"].append(auth["auth__permission_url"])
            permissions_dict[auth["role_id"]]["action"].append(auth["auth__act"])
    return permissions_dict