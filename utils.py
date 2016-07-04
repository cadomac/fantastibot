# utils.py
# Utility functions for bot.

import cfg
import urllib.request, json
import time, _thread
from time import sleep

# Function: chat
# Send a chat message to the server.
# Params:
# sock -- the socket over which to send the message
# msg -- the message to send

def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

# Function: ban
# Ban a user from the channel
# Params:
# sock -- socket over which to send ban command
# user -- the user to be banned

def ban(sock, user):
    chat(sock, ".ban {}".format(user).encode("utf-8"))

# Function: timeout
# Timeout a user for a set period of time
# Params:
# sock -- socket over which to send timeout comm
# user -- user to be timed out
# seconds -- length of timeout in seconds

def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds).encode("utf-8"))

# Function: threadFillOpList
# In a separate thread, fill up the op list

def threadFillOpList():
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/twistedethernet/chatters'
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            response = urllib.request.urlopen(req).read().decode()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"]["global_moderators"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"]["admin"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    cfg.oplist[p] = "staff"
        except:
            'do nothing'
        sleep(5)


def isOp(user):
    return user in cfg.oplist
