
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# InstagramAPI repo : https://github.com/LevPasha/Instagram-API-python
# APscheduler  repo : https://github.com/agronholm/apscheduler/
from datetime import datetime
import time
import os
import random

from apscheduler.schedulers.background import BackgroundScheduler

from instagram_private_api import Client


#Import PIL in order to know picture's size and to add watermarks
from PIL import Image, ImageFont, ImageDraw

from termcolor import colored, cprint


##############################
#        Directory Tree      #
##############################

"""
Instabot Directory Tree
 |
 |-- Instabot.py: the python script bot
 |
 |-- accounts.txt: file which contains the accounts and their proxys ip
 |                 proxy format: http://127.0.0.1:8888
 |                 account:password:proxy (each line)
 |                 contents: "account:|:password:|:proxy
 |                            account:|:password:|:proxy
 |                            account:|:password:|:proxy"
 |                 /\
 |                /!!\  proxy address must be replace by None if you don't want use proxy
 |               /_!!_\
 |
 |-- account directory: 1 directory for each account
        |
        |-- settings.txt: file wich contains device_id, uuid, phone_id
        |                 contents: "device_id=device_id
        |                            uuid=uuid
        |                            phone_id=phone_id
        |                            watermark=text or image or n
        |                            watermark_text=watermark_text if use
        |                            font_file=font_path if use
        |                            watermark_file=watermark_path if use"
        |
        |                   font and watermark file name must be full with their extension
        |                   font and watermark file must be in the same directory as settings.txt
        |
        |
        |-- tmp: directory containing photos to upload after watermark process
        |
        |-- photos: directory containing photos to upload
"""

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

        # # # # # # # # # # # # # # #
        # HERE WE ADD THE CRON JOBS #
        # # # # # # # # # # # # # # #


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


        # Activity jobs

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


#Add watermark on image
#Add watermark from text
def add_watermark(image, final_image_path, watermark_text, font_path):
	image_width, image_height = image.size

	#Create final image
	final_image_width, final_image_height = image_width, image_height + image_height / 10
	final_image = Image.new("RGBA", (int(image_width), int(final_image_height)), color=(255,255,255))

	#Past the picture on the final image
	final_image.paste(image, (0,0))

	#Write watermarks
	draw = ImageDraw.Draw(final_image)
	font_size = int(image_height * image_width /3500) #15000 bestvacations, 7000 videos.ouf
	font = ImageFont.truetype(font_path, font_size) #FONT TRUETYPE only
	x, y = draw.textsize(watermark_text, font = font) #text dimensions

	x2 = (final_image_width - x) / 2
	y2 = image_height + ((final_image_height - image_height) - y) / 2
	draw.text((x2, y2), watermark_text, (0,0,0), font=font)

	#Save the final image which is ready to be uploaded
	final_image.save(final_image_path)

#Add watermark from image
def add_watermark_from_image(image, final_image_path, watermark_path):
	image_width, image_height = image.size

	#Open watermark image
	watermark = Image.open(watermark_path)

	#Resize the watermark
	watermark_width, watermark_height = watermark.size
	watermark = watermark.resize( ( int(image_width/3*(image_width/watermark_width)), int(image_height/3*(image_height/watermark_height)) ))

	#Paste the watermark on the image wich will be posted on IG
	image.paste(watermark, (0,0), watermark)

	#Save the final image in the indicated directory
	image.save(final_image_path)

#Add watermark
def add_watermark(account, image, final_image_path):
    settings = open(account + "/settings.txt", "r").read().splitlines()
    if settings[3].split("=")[-1]=="text":
        add_watermark_from_text(image, final_image_path, settings[4].split("=")[-1], account+"/"+settings[5].split("=")[-1])
    if settings[3].split("=")[-1]=="image":
        add_watermark_from_image(image, final_image_path, account+"/"+settings[6].split("=")[-1])
    else:
        #No Watermark
        #Save image in tmp directory
        image.save(final_image_path)


# Create the InstagramAPI instances for each account
def create_ig_api_instances(accounts_filename):
    try:
        # Open file which contains the accounts and their proxys ip and split lines
        accounts_raw = open(accounts_filename, 'r').read().splitlines()


        # Split account:password:proxy
        #Proxy format exemple ‘http://127.0.0.1:8888'
        global accounts
        accounts= []
        for i in range(0, len(accounts_raw)):
            accounts.append(accounts_raw[i].split(":|:"))


        # Create InstagramAPI instance for each account
        # First initialize the instance global list
        global instance
        instance = []
        for i in range (0, len(accounts_raw)):
            instance.append(i)

        # Then create the different instances
        for i in range(0, len(accounts)):
            # Open file wich contains device_id, uuid, phone_id for each account (1 line for each parameter)
            try:
                settings = open(accounts[i][0] + "/settings.txt", "r").read().splitlines()
                instance[i] = Client(accounts[i][0], accounts[i][1],
                    proxy=accounts[i][2],
                    device_id=settings[0].split("=")[-1],
                    uuid=settings[1].split("=")[-1],
                    phone_id=accounts[2].split("=")[-1])
            except:
                # No files containing settings
                instance[i] = Client(accounts[i][0], accounts[i][1], proxy=accounts[i][2])
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
            pics_dir_path = "{0}/{1}/photos".format(actual_dir_path, accounts[number][0])

            # Chose a random pic inside
            chosen_pic = random.choice(os.listdir(pics_dir_path))

            # Determine what is the full path of the chosen pic
            final_pic_path = "{0}/{1}".format(pics_dir_path, chosen_pic)
            #print(pics_dir_path)
            #print(final_pic_path)

            # Find and verify the extension (must be jpg or jpeg)
            pic_extension = chosen_pic.split('.')[-1]


            # Configure & Upload the pic
            if pic_extension == 'jpg' or extension == 'jpeg':
                #Open image
                picture = Image.open(final_pic_path)
                #Add watermark
                tmp_file_path = "{0}/{1}/tmp/tmp.jpeg".format(actual_dir_path, accounts[number][0])
                add_watermark(accounts[number][0], picture, tmp_file_path)

                # Find the picture's size and set it in a tuple which is required by the upload function
                picture = Image.open(tmp_file_path)
                width, height = picture.size
                size = (width, height)

                # Upload the pic
                instance[number].post_photo(open(tmp_file_path, 'rb').read(), size, get_caption(number))
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
