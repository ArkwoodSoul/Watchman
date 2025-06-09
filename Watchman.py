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
ua = "{} using Watchman, by The Phantom Gambler and DragoE".format(data["user_agent"])
sans.set_agent(ua)
# defining the target region
regions = [x.lower().replace(" ","_") for x in data["target_regions"]]
#Initialize region size counter
region_pops = 0
for region in regions:
    response = sans.get(sans.Region(region,"numnations")).xml
    region_pops += int(response.find(".//NUMNATIONS").text)
embed = discord.Embed(title="Watchman Online",description="Watchman is looking out for {} which currently have a total of {} nations".format(", ".join([x.replace("_"," ").title() for x in regions]),region_pops),color=discord.Color(data["information_c"]))
WebhookSync.send(embed=embed)
# The heart of the program, retrieves the information we want and posts to webhook URL
try:
    for event in sans.serversent_events(sans.Client(),"cte","move").view(regions=regions):
        event_text = event["str"]
        if "relocated" in event_text:
            if any("from %%{}%%".format(region) in event_text for region in regions):
                nname = re.search(r"@@(.*)@@",event_text).group(1)
                link = "https://www.nationstates.net/nation={}".format(nname)
                region_pops -= 1
                final_msg = "[{}]({}) {}. Current population {}".format(nname.replace("_"," ").title(),link,data["leave"],region_pops) #link + " has departed The Brotherhood."
                embed = discord.Embed(title="Departure",description=final_msg,color=discord.Color(data["leave_c"]))
                WebhookSync.send(embed=embed)
            else:
                nname = re.search(r"@@(.*)@@",event_text).group(1)
                link = "https://www.nationstates.net/nation={}".format(nname)
                region_pops += 1
                final_msg = "[{}]({}) {}. Current population {}".format(nname.replace("_"," ").title(),link,data["join"],region_pops) #link + " has joined The Brotherhood."
                embed = discord.Embed(title="Arrival",description=final_msg,color=discord.Color(data["join_c"]))
                WebhookSync.send(embed=embed)
        else:
            nname = re.search(r"@@(.*)@@",event_text).group(1)
            link = "https://www.nationstates.net/nation={}".format(nname)
            region_pops -= 1
            final_msg = "[{}]({}) {}. Current population {}".format(nname.replace("_"," ").title(),link,data["cte"],region_pops) #link + " has died in service to The Overseer."
            embed = discord.Embed(title="Entombment",description=final_msg,color=discord.Color(data["data_c"]))
            WebhookSync.send(embed=embed)
except KeyboardInterrupt:
    #Slightly more gracefull exit
    embed = discord.Embed(title="Watchman Offline",description="Watchman session has been shut down",color=discord.Color(data["information_c"]))
    WebhookSync.send(embed=embed)
except Exception as e:
    #For if some reason something goes wrong
    print(e)
    embed = discord.Embed(title="Watchman Error",description="Watchman encountered an unexpected exception and has stopped.",color=discord.Color(data["information_c"]))
    WebhookSync.send(embed=embed)