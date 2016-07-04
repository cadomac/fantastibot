# bot.py
# Back-end of bot

import cfg
import utils
import socket
import re
import time, _thread
from time import sleep

def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")

    _thread.start_new_thread(utils.threadFillOpList, ())

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)

            # Custom commands
            if message.strip() == "!time":
                utils.chat(s, "It is currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))
            if message.strip() == "Hello FantastiBot!":
                utils.chat(s, "Hello " + username + "!")
            if message.strip() == "!mods":
                modlist = []
                for i in cfg.oplist:
                    if cfg.oplist[i] == "mod":
                        modlist.append(i)
                if len(modlist) == 0:
                    utils.chat(s, "There are no moderators currently online.")
                elif len(modlist) == 1:
                    utils.chat(s, "Currently, " + modlist[0] + " is the only moderator online.")
                elif len(modlist) >= 2:
                    modString = ""
                    for i in range(len(modlist)):
                        if i == len(modlist)-1:
                            modString += modlist[i]
                        elif i == len(modlist)-2:
                            modString += modlist[i] + " and "
                        elif i < len(modlist)-2:
                            modString += modlist[i] + ", "
                    utils.chat(s, modString + " are currently moderating.")

            # Custom OP commands
            if utils.isOp(username):
                if message.strip() == "!messages":
                    utils.chat(s, "Please follow me, I don't bite.")
                    utils.chat(s, "I'm so lonely.")
                if message.strip().find("!timeout") != -1:
                    utils.timeout(s, message[9:])
        sleep(1)

if __name__ == "__main__":
    main()
