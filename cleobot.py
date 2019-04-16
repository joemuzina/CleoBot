'''
    CleoBot
    Developed by Joe Muzina
    joe.muzina@gmail.com
    Last updated 4/12/2019
'''
import os
import random
import tweepy
import api_data

cleobot_version = "1.1"

# -1 for normal execution, song index for song debugging
debug = -1
post_tweet = True

# list of song files to pull phrases from
playlist = ["youth.txt",              # 0
            "hometown.txt",           # 1
            "bernard_trigger.txt",    # 2
            "the_depths.txt",         # 3
            "daphne_did_it.txt",      # 4
            "chromeo.txt",            # 5
            "city_kids.txt",          # 6
            "belly_button_blues.txt", # 7
            "friends.txt",            # 8
            "sanjake.txt"             # 9
            ]

# Print every phrase from a song and its length
def cleo_debug():
    for i in range(len(phrases)):
        if len(phrases[i]) > 1:
            print("Phrase length:")
            print(len(phrases[i]))
            if i == 0:
                print(phrases[i][0: len(phrases[i])] + "\n")
            else:
                print(phrases[i][2: len(phrases[i])] + "\n")

# Get a random phrase from a random song
def get_phrase():
    # Read in our most recent tweet
    check_last = open(resource_path("cleo_data/last_phrase.txt"))
    last_msg = check_last.read()
    check_last.close()
    
    last_matched = True
    
    # Generate tweet. If the tweet matches our most recent tweet, pick a new random
    # Phrase until we have a phrase that does not match the most recent tweet.
    while last_matched:
        # String split function also returns some strings with blank spaces.
        # This loop ensures that the random tweet will not be a blank space.
        while True:
            rand_num = random.randint(1, len(phrases) - 1)
            if len(phrases[rand_num]) > 1:
                break
        
        random_phrase = phrases[rand_num]
        
        # If the phrase is the first of the song, use it as the random phrase outright.
        # Otherwise, remove the first two characters (a blank space and a new line) and use that.
        if rand_num != 0:
            random_phrase = random_phrase[2: len(random_phrase)]

        if random_phrase == last_msg:
            print("Randomly selected tweet matched Cleobot's most recent tweet!\nRe-drawing...\n")
            continue
        else:
            last_matched = False # Set flag that we are done searching for a random phrase

        # Write random phrase to a data file so that the next tweet does not match it
        last_phrase = open(resource_path("cleo_data/last_phrase.txt"), "w")
        last_phrase.write(random_phrase)
        last_phrase.close()
        
        return random_phrase

# Get API info
def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

# Gets directory of data files within executable temp directory
# Credit to max at StackOverflow for this function
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if debug > - 1:
    song_pick = playlist[debug] # Sets song to specified debug index
else:
    song_pick = playlist[random.randint(0, len(playlist) - 1)] # Randomly selects song

# Open selected song file and read it in
file = open(resource_path("cleo_data/" + song_pick))
file_string = file.read()
phrases = file_string.split(";") # Split song into a list of phrases

if debug > -1:
    cleo_debug()
else:
    tweet = get_phrase()
    if post_tweet:
        api = get_api(api_data.api_cfg)
        print("\n-----Cleobot v" + cleobot_version + " Initialized-----\nRandomly selected phrase: \n\n" + tweet + "\n")
        api.update_status(tweet)
        if api:
            print("Tweet published successfully!\n-----------------------------------\n")
    else:
        print("\nRandomly selected phrase:\n" + tweet + "\n")
