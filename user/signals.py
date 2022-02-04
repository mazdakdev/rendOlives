
def my_callback(sender, **kwargs):
    print("Request finished")


def create_new_user(sender, instance, created, **kwargs):
    if created:
        print("new user", instance)


def update_user(sender, instance, created, **kwargs):
    if not created:
        print("update user", instance)
