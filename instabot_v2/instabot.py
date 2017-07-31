#!/usr/bin/env python
# -*- coding: utf-8 -*-

# InstagramAPI repo : https://github.com/LevPasha/Instagram-API-python
# APscheduler  repo : https://github.com/agronholm/apscheduler/
from datetime import datetime
import time
import os
import random

from apscheduler.schedulers.background import BackgroundScheduler
from InstagramAPI import InstagramAPI


##############################
#      APScheduler jobs      #
##############################

# Setup the scheduler
def scheduler_setup():

        # We initialize the APScheduler BackgroundScheduler
        global scheduler
        scheduler = BackgroundScheduler()

# Here we define the scheduler jobs and we start the scheduler
def scheduler_start_n_go():
        # Add the cron jobs (Instagram bots)
        #scheduler.add_job(lambda: tick("tickk"), 'cron', second=15, timezone="Europe/Paris")
        scheduler.add_job(tick, 'cron', args= ['tickk'], second=15, timezone="Europe/Paris")
        # Start the Background Scheduler
        scheduler.start()


#############################
#       Instabot jobs       #
#############################

# Create the InstagramAPI instances for each account
def create_ig_api_instances(accounts_filename):
    try:
        # Open file which contains the accounts and split lines
        accounts_raw = open(accounts_filename, 'r').read().splitlines()


        # Split account:password
        global accounts
        accounts= []
        for i in range(0, len(accounts_raw)):
            accounts.append(accounts_raw[i].split(':'))


        # Create InstagramAPI instance for each account
        # First initialize the instance global list
        global instance
        instance = []
        for i in range (0, len(accounts_raw)):
            instance.append(i)

        # Then create the different instances
        for i in range(0, len(accounts)):
            instance[i] = InstagramAPI(accounts[i][0], accounts[i][1])

    except ValueError as err:
        print(err.args)



# Log in to Instagram for each account
def login_ig_api_instances():
        # For each instance we log in to Instagram
        for i in range(0, len(instance)):
            instance[i].login()



# Log out to Instagram for each account
def logout_ig_api_instances():
        # For each instance we log out of Instagram
        for i in range(0, len(instance)):
            instance[i].logout()



# Generate a random caption from the account Number and his captions list
def get_caption(number):
        try:
            actual_dir_path = os.path.dirname(os.path.realpath(__file__))
            captions_location_path = "{0}/captions/{1}.txt".format(actual_dir_path, accounts[number][0])
            captions_raw = open(captions_location_path).read().split("_-_-_\n")

            return random.choice(captions_raw)

        except ValueError as err:
            print(err.args)


# Upload a photo to the account Number (using his pics folder and get_caption())
def upload_photo(number):
        try:
            # Chose random picture from the right folder
            # First find what is the actual directory path
            actual_dir_path = os.path.dirname(os.path.realpath(__file__))

            # Then determine what is the correspondant pics directory path
            pics_dir_path = "{0}/pics/{1}".format(actual_dir_path, accounts[number][0])

            # Chose a random pic inside
            chosen_pic = random.choice(os.listdir(pics_dir_path))

            # Determine what is the full path of the chosen pic
            final_pic_path = "{0}/{1}".format(pics_dir_path, chosen_pic)
            #print(pics_dir_path)
            #print(final_pic_path)

            # Find and verify the extension (must be jpg or jpeg)
            pic_extension = chosen_pic.split('.')[-1]

            # Upload the pic
            if pic_extension == 'jpg' or extension == 'jpeg':

                instance[number].uploadPhoto(final_pic_path, get_caption(number))

            else:
                print("error with file :(")
        except ValueError as err:
            print(err.args)



# Job to simulate a real activity on the account (to be continued)
def simulate_random_activity(number):
        time.sleep(random.randint(0,7200))
        instance[number].syncFeatures()
        instance[number].autoCompleteUserList()
        instance[number].timelineFeed()
        instance[number].getv2Inbox()
        instance[number].getRecentActivity()

# To use before posting anything /!\ BE CAREFUL IT'S IMPORTANT /!\
def simulate_activity(number):
        instance[number].syncFeatures()
        instance[number].autoCompleteUserList()
        instance[number].timelineFeed()
        instance[number].getv2Inbox()
        instance[number].getRecentActivity()

# This job simply combine simulate_activity and upload_photo
def complete_uploading_photo_deluxe(number):
        simulate_activity(number)
        upload_photo(number)


#DEVELOPEMENT
def tick(tick):
        print(tick)




####################################
#              MAIN                #
####################################


if __name__ == '__main__':

    # First, we create an IG API instance for each account provided in the account list .txt file
    create_ig_api_instances("accounts.txt")
    # Then we log in to Instagram each instance/account
    login_ig_api_instances()
    upload_photo(0)
    logout_ig_api_instances()

    # We log in each API instance
    #login_ig_api_instances()
    # WHILE DEVELOPEMENT
    #logout_ig_api_instances()

    # Start the scheduler for instabot!
    # Instabot just started!


    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        logout_ig_api_instances()
