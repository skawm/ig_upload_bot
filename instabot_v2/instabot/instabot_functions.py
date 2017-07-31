#!/usr/bin/env python
# -*- coding: utf-8 -*-

# InstagramAPI repo : https://github.com/LevPasha/Instagram-API-python
# APscheduler  repo : https://github.com/agronholm/apscheduler/
from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from InstagramAPI import InstagramAPI


class Instabot:

    def create_ig_api_instances(accounts_filename):

        # Open file which contains the accounts and split lines
        accounts_raw = open(accounts_filename, 'r').read().splitlines()


        # Split account:password
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



    def login_ig_api_instances():
        # For each instance we log in to Instagram
        for i in range(0, len(instance)):
            instance[i].login()

    def logout_ig_api_instances(): # for DEVELOPEMENT only
        # For each instance we log out of Instagram
        for i in range(0, len(instance)):
            instance[i].logout()


    def scheduler_setup_n_go():

        # We initialize the APScheduler BackgroundScheduler
        global scheduler
        scheduler = BackgroundScheduler()

        # Add the cron jobs (Instagram bots)
        #scheduler.add_job(lambda: tick("tickk"), 'cron', second=15, timezone="Europe/Paris")
        scheduler.add_job(tick, 'cron', args= ['tickk'], second=15, timezone="Europe/Paris")

        # Start the Background Scheduler
        scheduler.start()



    # Instabot job
    def upload_photo(instance):
        # All arguments are required
        print("fake uploading")
        # Initialize InstagramAPI and login to Instagram






    def tick(tick): #DEVELOPEMENT
        print(tick)
