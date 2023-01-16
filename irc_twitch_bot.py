import os
import sys
import irc.bot
import requests
from datetime import datetime

# Twitch v5 API Create Client ID: https://dev.twitch.tv/console/apps/create
# Twitch v5 API Token: https://dev.twitch.tv/docs/authentication#getting-tokens

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        request = requests.get(url, headers=headers).json()
        self.channel_id = request['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], 'chatty_the_chat_bot', 'chatty_the_chat_bot')

    def on_welcome(self, connection, event):
        print('Joining ' + self.channel[1:])

        # You must request specific capabilities before you can use them
        connection.cap('REQ', ':twitch.tv/membership')
        connection.cap('REQ', ':twitch.tv/tags')
        connection.cap('REQ', ':twitch.tv/commands')
        connection.join(self.channel)

    def on_pubmsg(self, connection, event):
        message = {}

        message['msg'] = event.arguments[0]

        for tag in event.tags:
            if tag['key'] == 'display-name':
                message['username'] = tag['value']
            if tag['key'] == 'user-id':
                message['userid'] = tag['value']
            if tag['key'] == 'mod':
                message['mod'] = tag['value']
            if tag['key'] == 'subscriber':
                message['subscriber'] = tag['value']

        if event.arguments[0][:1] == '!':
            message['commands'] = event.arguments[0].split(' ')[0][1:]
        else:
            message['commands'] = ''

        print(f'{datetime.now()}: {message}')
        return

def main(client_id, token, channel):
    bot = TwitchBot(client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(os.getenv("API_KEY"), os.getenv("API_SECRET"), args[0])
