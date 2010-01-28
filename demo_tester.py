#!/usr/bin/env python
import random
from django.core.management import setup_environ
import settings

setup_environ(settings)

from demo.models import *
from demo.utils import *

print "This program is used to test the query speeds of the demo app given different sizes of Users, Groups and Records."
print "For accurate results make sure to delete all demo.* tables in your database first and rerun the syncdb command."

num_of_users = int(raw_input("How many users would you like to create? "))
print "Creating users..."
User.objects.create_test_users(num_of_users)

size_of_group = int(raw_input("How many users would you like to put in your new group? "))
print "Creating group..."
group = Group.objects.create_test_group(size_of_group)

print "We will randomly create records for each user based on a Gaussian distribution."
records_mean = int(raw_input("\tWhat would you like to set the mean to? "))
records_sigma = float(raw_input("\tAnd the sigma value? "))
print "Creating records (this could take a while)..."
Record.objects.create_random_records(records_mean, records_sigma)

print "Running Group tests..."
timeit(group.how_many_members)()
timeit(group.completed_actions_by_user)()
timeit(group.completed_actions_by_user_denorm)()
timeit(group.members_with_points)()
timeit(group.get_latest_records)()

users = User.objects.all()
user = users[random.randint(0, len(users) - 1)]
print "Running User tests..."
timeit(user.get_latest_records)()
timeit(user.get_total_points)()
timeit(user.actions_with_additions)()
timeit(user.get_chart_data)()

actions = Action.objects.all()
action = actions[random.randint(0, len(actions) - 1)]
print "Running Action tests..."
timeit(action.users_with_completes)()
timeit(action.users_with_completes_denorm)()
