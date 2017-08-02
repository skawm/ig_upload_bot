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

from termcolor import colored, cprint


banner = """
#### ##    ##  ######  ########    ###    ########   #######  ########
 ##  ###   ## ##    ##    ##      ## ##   ##     ## ##     ##    ##
 ##  ####  ## ##          ##     ##   ##  ##     ## ##     ##    ##
 ##  ## ## ##  ######     ##    ##     ## ########  ##     ##    ##
 ##  ##  ####       ##    ##    ######### ##     ## ##     ##    ##
 ##  ##   ### ##    ##    ##    ##     ## ##     ## ##     ##    ##
#### ##    ##  ######     ##    ##     ## ########   #######     ##
"""
##############################
#      APScheduler jobs      #
##############################

# Setup the scheduler
def scheduler_setup():

        # We initialize the APScheduler BackgroundScheduler
        global scheduler
        scheduler = BackgroundScheduler()

        # # # # # # # # # # # # # # #
        # HERE WE ADD THE CRON JOBS #
        # # # # # # # # # # # # # # #


        # Parameters:

        #year (int|str) – 4-digit year
        #month (int|str) – month (1-12)
        #day (int|str) – day of the (1-31)
        #week (int|str) – ISO week (1-53)
        #day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        #hour (int|str) – hour (0-23)
        #minute (int|str) – minute (0-59)
        #second (int|str) – second (0-59)
        #start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
        #end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
        #timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

        # To run a job, you'll need to specify the number of the account concerned. Take a look at your accounts.txt file:
        # 1st account (line 1) is number 0, 2nd account (line 2) is number 1, etc..



        # To include parameters into a job you can use args=[''] or use a lambda : func(args)
        # here's a sample job, written in the two possibility
        #scheduler.add_job(tick, 'cron', args= ['tickk'], second=15, timezone="Europe/Paris")
        #scheduler.add_job(lambda: tick("tickk"), 'cron', second=15, timezone="Europe/Paris")




        # /!\ MAKE SURE YOU DON'T POST TWO PICS IN THE SAME TIME /!\
        # Posting jobs
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=9, minute=30, timezone="Europe/Paris")  # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=11, minute=59, timezone="Europe/Paris") # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=16, minute=30, timezone="Europe/Paris") # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=16, minute=52, timezone="Europe/Paris") # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[0], hour=16, minute=59, timezone="Europe/Paris") # Smsdedingue
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=17, minute=5, timezone="Europe/Paris")  # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[0], hour=17, minute=9, timezone="Europe/Paris")  # Smsdedingue
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=17, minute=29, timezone="Europe/Paris") # Humourdebob
        scheduler.add_job(upload_photo_deluxe, 'cron', args=[1], hour=18, minute=0, timezone="Europe/Paris")  # Humourdebob

        # Activity jobs
        scheduler.add_job(simulate_random_activity, 'cron', args=[0], hour=7, minute=59, timezone="Europe/Paris")  # Smsdedingue
        scheduler.add_job(simulate_random_activity, 'cron', args=[1], hour=9, minute=59, timezone="Europe/Paris")  # Humourdebob
        scheduler.add_job(simulate_random_activity, 'cron', args=[0], hour=13, minute=25, timezone="Europe/Paris") # Smsdedingue
        scheduler.add_job(simulate_random_activity, 'cron', args=[1], hour=18, minute=04, timezone="Europe/Paris") # Humourdebob
        scheduler.add_job(simulate_random_activity, 'cron', args=[0], hour=20, minute=9, timezone="Europe/Paris")  # Smsdedingue
        scheduler.add_job(simulate_random_activity, 'cron', args=[1], hour=22, minute=9, timezone="Europe/Paris")  # Humourdebob
        scheduler.add_job(simulate_random_activity, 'cron', args=[0], hour=0, minute=9, timezone="Europe/Paris")   # Smsdedingue
        scheduler.add_job(simulate_activity, 'cron', args=[1], hour=2, minute=10, timezone="Europe/Paris")         # Humourdebob
        #dev
        #scheduler.add_job(upload_photo_deluxe, 'cron', args=[0], hour=21, minute=6, timezone="Europe/Paris" )

        cprint('Scheduler ready to go!', 'green')



# Here we define the scheduler jobs and we start the scheduler
def scheduler_start_n_go():
        # Simply start the Background Scheduler
        scheduler.start()
        cprint('Scheduler started!', 'green')

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
            cprint('Instance created for {0}'.format(accounts[i][0]), 'blue')

    except ValueError as err:
        print(err.args)



# Log in to Instagram for each account
def login_ig_api_instances():
        # For each instance we log in to Instagram
        for i in range(0, len(instance)):
            instance[i].login()
            time.sleep(10)
        cprint('Accounts just logged in :)', 'green')


# Log out to Instagram for each account
def logout_ig_api_instances():
        # For each instance we log out of Instagram
        for i in range(0, len(instance)):
            instance[i].logout()
            time.sleep(10)
        cprint('Accounts just logged out :)', 'green')


# Generate a random caption from the account Number and his captions list
def get_caption(number):
        try:
            actual_dir_path = os.path.dirname(os.path.realpath(__file__))
            captions_location_path = "{0}/captions/{1}.txt".format(actual_dir_path, accounts[number][0])
            captions_raw = open(captions_location_path).read().split("_-_-_\n")
            cprint('Caption generated', 'green')
            return random.choice(captions_raw)

        except:
            cprint('/!\ No caption generated', 'red')
            return ""


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
                cprint('Just uploaded a pic to {0}'.format(accounts[number][0]), 'green')

            else:
                cprint('error with picture to upload :(', 'red')

            # Remove the uploaded pic from the folder so we never gonna repost it
            os.remove(final_pic_path)
        except:
            cprint('/!\ No pic uploaded, need debug if persist', 'red')



# Job to simulate a real activity on the account (to be continued)
# To use before posting anything /!\ BE CAREFUL IT'S IMPORTANT /!\
def simulate_activity(number):
        instance[number].syncFeatures()
        time.sleep(1)
        instance[number].autoCompleteUserList()
        time.sleep(1)
        instance[number].timelineFeed()
        time.sleep(1)
        instance[number].getv2Inbox()
        time.sleep(1)
        instance[number].getRecentActivity()



def simulate_random_activity(number):
        time_to_sleep = random.randint(0,7200)
        cprint('Simulating random activity, gonna sleep for {0}'.format(str(time_to_sleep)), 'cyan')

        time.sleep(time_to_sleep)

        simulate_activity(number)


# This DELUXE job simply combine simulate_activity and upload_photo
def upload_photo_deluxe(number):
        time_to_sleep = random.randint(0,120)#300s
        cprint('Simulating random sleep before upload a pic, gonna sleep for {0}'.format(str(time_to_sleep)), 'cyan')
        time.sleep(time_to_sleep)
        cprint('Just sleeped well :)', 'cyan')
        simulate_activity(number)
        time.sleep(random.randint(7,15))
        upload_photo(number)


#DEVELOPEMENT
def tick(tick):
        print(tick)




####################################
#              MAIN                #
####################################


if __name__ == '__main__':
    # First, before EVERYTHING, we print a butiful ASCII logo
    cprint(banner, 'green')
    # Then, we create an IG API instance for each account provided in the account list .txt file
    create_ig_api_instances("accounts.txt")

    # Then we log in to Instagram each instance/account
    login_ig_api_instances()

    # Setup the scheduler for instabot! :)
    scheduler_setup()

    # Start the scheduler !! :)
    scheduler_start_n_go()

    # Instabot just started! :D

    cprint('Instabot just started! :)', 'cyan')
    cprint('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'), 'magenta')

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        # We shutdown the scheduler and we logout of each Instagram account
        cprint('shutdown, please wait for correct exit', 'red')
        scheduler.shutdown()
        logout_ig_api_instances()
