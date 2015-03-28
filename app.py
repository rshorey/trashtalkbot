import random
import os
import re
import sys
import datetime
import tweepy


def create_insult(usernames=None):
    nouns = ["team","bracket",
        "strategy","free throw percent",
        "point guard","mascot","t-shirt cannon","coach",
        "basketball","curtain of distraction",
        "shot clock","pair of tube socks",
        "ability to jump","dribble"]

    adjectives = ["stinky",
                    "dastardly",
                    "Machiavellian",
                    "serpentine",
                    "pseudorandom",
                    "outside the margin of error",
                    "full of eels",
                    "a hamster",
                    "the worst",
                    "incredibly creepy",
                    "chopped liver",
                    "a rampallion",
                    "a pile of deceased ferrets",
                    "a scurvy landlubber",
                    "as loathsome as a toad",
                    "a rotten banana",
                    "temporarily out of service",
                    "kaput",
                    "a shipment of improperly aged cheese",
                    "rotten in the state of Denmark",
                    "not going to space today",
                    "undribblable",
                    "tripe",
                    "jello",
                    "a load of malarkey",
                    "so 1999"]

    noun = random.choice(nouns)
    adj = random.choice(adjectives)
    if usernames:
        insult = "{names}, your {noun} is {adjective}. #marchmadness #trashtalk".format(names=usernames,noun=noun,adjective=adj)
    else:
        insult = "Your {noun} is {adjective}. #marchmadness #trashtalk".format(noun=noun,adjective=adj)
    return insult

def get_mentions(api):
    mentions = api.mentions_timeline(count=50)
    return mentions

def get_usernames(tweet,botname):
    usernames = re.findall(r'@[a-zA-Z0-9_]*',tweet)
    usernames.remove(botname)
    return usernames


minutes_since_last_run = int(sys.argv[1])
now = datetime.datetime.utcnow()
time_of_last_run = now - datetime.timedelta(minutes=minutes_since_last_run)

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



mentions = get_mentions(api)
mention_ids = []
for m in mentions:
    username = m.author.screen_name
    mention_id = m.id
    mention_ids.append(m.id)
    all_names = get_usernames(m.text,"@trashtalkbot")
    all_names.insert(0,"@"+username)
    usernames = " ".join(all_names)
    tweet_create_time = m.created_at

    insult = create_insult(usernames)

    #prevents tweeting if there's no start time
    #to prevent repeated spamming
    if tweet_create_time > time_of_last_run:
        api.update_status(status = insult, in_reply_to_status_id=mention_id)

if random.random() < .05:
    #randomly insult no one one out of 20 times
    insult = create_insult()
    api.update_status(status=insult)