from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from icon.models import *
from datetime import datetime


@receiver(pre_save, sender=Woman)
def post_save_woman_post(sender, instance, **kwargs):
    if len(instance.title) > 10: #if title in admin page is shorter than 10
        pass
    else:
        raise ValueError("Can't save that short title")    


def create_user(sender, instance, created, **kwargs):
    if created:
        Woman.objects.create(cat=instance)
        print("User Created")

post_save.connect(create_user, sender = User)

def update_user(sender, instance, created, **kwargs):
    if not created:
        print("User Updated")

post_save.connect(update_user, sender = User)

def create_post(sender, instance, created, **kwargs):
    if created:
        print("Profile Created")

post_save.connect(create_post, sender = Woman)

def update_post(sender, instance, created, **kwargs):
    if not created:
        print("Profile Updated")

post_save.connect(update_post, sender = Woman)


def user_sign_in(sender, user, request, **kwargs):
    if user and request:
        with open("icon/order_folders/in_out_list.txt", "a") as file:
            file.write(f"user '{user}' succesfully loged <IN> at '{datetime.now().strftime('%d-%m-%y %a %H:%M:%S')}' \n")

user_logged_in.connect(user_sign_in)

def user_log_out(sender, user, request, **kwargs):
    if user and request:
        with open("icon/order_folders/in_out_list.txt", "a") as file:
            file.write(f"user '{user}' succesfully loged <OUT> at '{datetime.now().strftime('%d-%m-%y %a %H:%M:%S')}' \n")

user_logged_out.connect(user_log_out)

def user_log_fail(sender, user, request, **kwargs):
    if user and request:
        with open("icon/order_folders/failed_list.txt", "a") as file:
            file.write(f"user '{user}' FAILED to log in at '{datetime.now().strftime('%d-%m-%y %a %H:%M:%S')}' \n")

user_login_failed.connect(user_log_fail)