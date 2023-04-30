import discord
from discord.ext import commands
import json

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome.py cog is online")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f) 

        welcome_embed = discord.Embed(title=f"Welcome to {member.guild.name}", description=f"You are the {member.guild.member_count} Member!", color=discord.Color.random())

        welcome_embed.add_field(name="We all welcome you to our server!", value=data[str(member.guild.id)]["Message"], inline=False )
        welcome_embed.set_thumbnail(url=member.guild.icon)
        welcome_embed.set_image(url=data[str(member.guild.id)]["ImageUrl"])
        welcome_embed.set_footer(text=f"Glad you joined!", icon_url=member.avatar)

        auto_role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]["AutoRole"])

        await member.add_roles(auto_role)

        if data[str(member.guild.id)]["Channel"] is None:
            await member.send(embed=welcome_embed)
        elif data[str(member.guild.id)]["Channel"] is not None:

            welcome_channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])

            await welcome_channel.send(embed=welcome_embed)


    @commands.group(name="welcome", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):

        info_embed = discord.Embed(title="Welcome System Setup", description="Create a unique welcome system for your server", color=discord.Color.teal())
        info_embed.add_field(name="autorole", value="Set automatic role so when a user joins they will recieve it automatically.", inline=False)
        info_embed.add_field(name="message", value="Set a message to be included in your welcome card.", inline=False)
        info_embed.add_field(name="channel", value="Set a channel for your welcome card to be sent in.", inline=False)
        info_embed.add_field(name="img", value="Set a image or gif url to be sent with the welocome card.", inline=False)
        
        await ctx.send(embed=info_embed)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["AutoRole"] = str(role.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, msg):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)


        data[str(ctx.guild.id)]["Message"] = str(msg)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

    @welcome.command()
    @commands.has_permissions(administrator=True)
    async def img(self, ctx, *, url):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["ImageUrl"] = str(url)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)


async def setup(client):
    await client.add_cog(Welcome(client))

