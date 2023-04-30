import discord
from discord.ext import commands
import os 
import asyncio
import json


client = commands.Bot(command_prefix=",", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Success: bot is connected to Discord")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_guild_join(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data[str(guild.id)] = {}
    data[str(guild.id)]["Channel"] = None
    data[str(guild.id)]["Message"] = None
    data[str(guild.id)]["AutoRole"] = None
    data[str(guild.id)]["ImageUrl"] = None
    
    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data.pop(str(guild.id))
    
    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)


async def main():
    async with client:
        await load()
        await client.start("")


asyncio.run(main())
