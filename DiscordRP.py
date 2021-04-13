import json
from pypresence import Presence

class DiscordRP:

    def __init__(self):
        self.loadClientID()
        self.RPC = Presence(self.client_id)
        self.RPC.connect()

    def loadClientID(self):
        with open('auth.json') as json_file:
            d = json.load(json_file)
            self.client_id = d['client_id']

    def updatePresence(self, info):
        options = {
            'state': 'Origin {}'.format(info['app'][:info['app'].index('.')]),
            'details': '{} by {}'.format(info['title'], info['album_artist'])
        }
        self.RPC.update(**options)
