def unix_user(principal):
    return principal.split("@")[0]

def get_user_home_dir(user):
    return '/home/' + user + '/'