Get real-time stream of chat messages (IRC) from a live Twitch streamer's chat. Provide username of live streamer as argument when starting program and stream will automatically begin.  The ouput will be a dictionary that has the chat message, username, whether the user is a mod, whether the user is a subscriber to the channel, and any commands in the message that start with "!".

API keys provided in this program may become out-of-date and stop working.  If this happens you can replace API client ID and token with your own (generated on Twitch's website and requires a free account).

**Example:**

python irc_twitch_bot.py pokimane

![image](https://user-images.githubusercontent.com/35471104/130335599-0e0802e9-d4cf-4b5b-86dd-bf247d1a612e.png)


