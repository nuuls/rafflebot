import random
import time
import logging

from threading import Thread

from bot import Bot
from config import EMOTES, CHANNELS

class Main:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.bot = Bot()
        self.bot.conn()
        self.bot.join("nuulsbot")
        self.q = self.bot.q
        Thread(target=self.listen).start()

    def getUser(self, line):
        seperate = line.split(":", 2)
        user = seperate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        separate = line.split(":", 2)
        message = separate[2]
        return message

    def getChannel(self, line):
        seperate = line.split("#", 1)
        channel = seperate[1].split(" ")[0]
        return channel

    def joinRaffle(self, msg, channel, t):
        logging.info("joining raffle in %s seconds" % str(t))
        time.sleep(t)
        self.bot.say(msg, channel)


    def listen(self):
        while True:
            line = self.q.get()

            if "PRIVMSG" in line:
                user = self.getUser(line)
                msg = self.getMessage(line)

                logging.info("%s: %s" % (user, msg))

                try:
                    if user == "nuulsbot":
                        msg = msg.split(":")
                        channel = msg[0]
                        if msg[1] == "raffle":
                            command = "!join "
                        t = random.randint(1, int(msg[2]))
                        tempmsg = command + random.choice(EMOTES)
                        if channel in CHANNELS:
                            Thread(target=self.joinRaffle, args=((tempmsg, channel, t))).start()
                except:
                    logging.exception("failed to read command")

            else:
                logging.debug(line)


Main()