import socket
import time
import logging
from queue import Queue

from threading import Thread

from config import *


class Bot:

    def __init__(self):
        logging.basicConfig(level=logging.debug)
        self.last_msg_sent = 0
        self.q = Queue()

    def conn(self):
        self.s = socket.socket()
        self.s.connect(("irc.chat.twitch.tv", 80))
        self.send_raw("PASS " + PASS)
        self.send_raw("NICK " + NICK)
        self.send_raw("CAP REQ :twitch.tv/commands")
        logging.info("connected")
        Thread(target=self.listen).start()
        Thread(target=self.ping).start()

    def join(self, channel):
        self.send_raw("JOIN #" + channel)
        logging.info("joined " + channel)

    def join_channels(self):
        for channel in CHANNELS:
            self.join(channel)
            self.raffle[channel] = False
        time.sleep(5)

    def send_raw(self, msg):
        self.s.send((msg + "\r\n").encode("utf-8"))

    def say(self, msg, channel):
        if self.last_msg_sent + 1.6 < time.time():

            if msg.startswith("."):
                space = ""
            else:
                space = ". "

            msgTemp = "PRIVMSG #" + channel + " :" + space + msg
            self.send_raw(msgTemp)
            try:
                logging.info("sent: " + msg)
            except:
                logging.warning("message sent but could not print")
            self.last_msg_sent = time.time()

    def ping(self):
        while True:
            try:
                while True:
                    time.sleep(120)
                    self.send_raw("PING")
            except:
                logging.warning("reconnecting in 30 seconds...")
                time.sleep(30)
                self.conn()
                return


    def listen(self):

        readbuffer = ""
        while True:

            readbuffer = readbuffer + (self.s.recv(2048)).decode("utf-8", errors="ignore")
            temp = readbuffer.split("\r\n")
            readbuffer = temp.pop()

            for line in temp:
                if line.startswith("PING"):
                    self.send_raw(line.replace("PING", "PONG"))
                elif not line.startswith("PONG"):
                    self.q.put(line)