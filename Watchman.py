import tomllib
import sans
import re
import discord
# opening and reading the config file
with open("Config.toml", "rb") as watchman:
    data = tomllib.load(watchman)
# defining webhook URL
webhook = data["url"]
WebhookSync = discord.SyncWebhook.from_url(webhook)
# defining the user agent and sending it to NS
ua = "{} using Watchman, by The Phantom Gambler".format(data["user_agent"])
sans.set_agent(ua)
# defining the target region
region = [x.lower().replace(" ","_") for x in data["target_regions"]]
# The heart of the program, retrieves the information we want and posts to webhook URL
for event in sans.serversent_events(sans.Client(),"cte","move").view(regions=region):
    event_text = event["str"]
    if "relocated" in event_text:
        if "from %%the_brotherhood_of_malice%%" in event_text:
            nname = re.search(r"@@(.*)@@",event_text).group(1)
            link = "https://www.nationstates.net/nation={}".format(nname)
            final_msg = "[{}]({}) {}".format(nname.replace("_"," ").title(),link,data["leave"]) #link + " has departed The Brotherhood."
            embed = discord.Embed(title="Departure",description=final_msg,color=discord.Color(data["leave_c"]))
            WebhookSync.send(embed=embed)
        else:
            nname = re.search(r"@@(.*)@@",event_text).group(1)
            link = "https://www.nationstates.net/nation={}".format(nname)
            final_msg = "[{}]({}) {}".format(nname.replace("_"," ").title(),link,data["join"]) #link + " has joined The Brotherhood."
            embed = discord.Embed(title="Arrival",description=final_msg,color=discord.Color(data["join_c"]))
            WebhookSync.send(embed=embed)
    else:
        nname = re.search(r"@@(.*)@@",event_text).group(1)
        link = "https://www.nationstates.net/nation={}".format(nname)
        final_msg = "[{}]({}) {}".format(nname.replace("_"," ").title(),link,data["cte"]) #link + " has died in service to The Overseer."
        embed = discord.Embed(title="Entombment",description=final_msg,color=discord.Color(data["data_c"]))
        WebhookSync.send(embed=embed)
