import random
import os
import re
import tweepy


def create_insult(usernames=None):
    nouns = ["team","bracket",
        "strategy","free throw percent",
        "point guard","mascot","t-shirt cannon","coach"]

    adjectives = ["stinky","small","hackable",
                    "dastardly","Machiavellian",
                    "irresponsible","serpentine",
                    "deflated","a loser","going down",
                    "doomed","flat-footed","pseudorandom",
                    "outside the margin of error","full of eels",
                    "a hamster"]

    noun = random.choice(nouns)
    adj = random.choice(adjectives)
    if usernames:
        insult = "{names}, your {noun} is {adjective}. #marchmadnesstrashtalk".format(names=usernames,noun=noun,adjective=adj)
    else:
        insult = "Your {noun} is {adjective}. #marchmadnesstrashtalk".format(noun=noun,adjective=adj)
    return insult

def get_mentions(api,last_id):
    if last_id:
        mentions = api.mentions_timeline(since_id=last_id)
    else:
        mentions = api.mentions_timeline()
    return mentions

def get_usernames(tweet,botname):
    usernames = re.findall(r'@[a-zA-Z0-9_]*',tweet)
    usernames.remove(botname)
    return usernames


CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

with open("last_tweet_file.txt",'r') as f:
    last_mention_id = f.read()

mentions = get_mentions(api,last_mention_id)
mention_ids = []
for m in mentions:
    username = m.author.screen_name
    mention_id = m.id
    mention_ids.append(m.id)
    all_names = get_usernames(m.text,"@trashtalkbot")
    all_names.insert(0,"@"+username)
    usernames = " ".join(all_names)

    insult = create_insult(usernames)

    #prevents tweeting if there's no start time
    #to prevent repeated spamming
    if last_mention_id:  
        api.update_status(status = insult, in_reply_to_status_id=mention_id)

if len(mention_ids) > 0:
    new_id = str(max(mention_ids))
    with open("last_tweet_file.txt",'w') as f:
        f.write(new_id)