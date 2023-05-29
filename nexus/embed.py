from discord import Embed
from profiles import Developer
from profiles import Bot
class EmbedsCreator():
    descriptions = {"commandDoesntExists" : "This command doesn't exist. Enter `!help` to get more information","default ": "Something unexpected and strage happened.Enter `!help` to get more information."}
    @staticmethod
    def errorEmbed(descriptions = "Something unexpected and strange happened.Enter `!help` to get more information."):
        embed = Embed(title="❌ Error!", color=0xff0000)
        embed.add_field(
            name="Details:",
            value=f"{descriptions}\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def emptyBugReport(descriptions = "Please provide a bug report."):
        embed = Embed(title="❌ Error!", color=0xff0000)
        embed.add_field(
            name="Details:",
            value=f"{descriptions}\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def reportForDev(reporter_info,bug_report):
        embed = Embed(title=":beetle: Bug Report", color=0xff0000)
        embed.add_field(name="Reporter : ", value=reporter_info, inline=False)
        embed.add_field(name="Bug Report : ", value=bug_report, inline=False)
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def showTheReport(reporter,bug_report):
        embed = Embed(title=":pray: thanks you for reporthing the bug!", color=0x00ff00)
        embed.add_field(name="author  : ", value=reporter, inline=False)
        embed.add_field(name="your bug report : ", value=bug_report, inline=False)
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def errorForEmbedLimitation(minutes,seconds):
        embed = Embed(title="❌ Error!", color=0xff0000)
        embed.add_field(
            name="Details:",
            value=f"Sorry, you can only report one bug per hour. Please try again in {minutes} minutes and {seconds} seconds.\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def pingEmbed(latency):
        embed = Embed(
        title="Ping",
        description=f":ping_pong: Pong! Latency: {latency}ms",
        color=0x0099ff)
    
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def chatGPT():
        embed = Embed(title="ChatGPT Channel", description="enter ```!start``` to create a text channel in order to chat\nthis message will be deleted in the next 5 seconds", color=0x0099ff)
    
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    
    @staticmethod
    def noPermission():
        embed = Embed(title="❌ Error!", color=0xff0000)
        embed.add_field(
            name="Details:",
            value="you don't have the permission to do that!\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        
        return embed
    @staticmethod
    def help():
        embed = Embed(title=":white_check_mark: Help", description="List of available commands :", color=0x00ff00)
        embed.add_field(name="```!ping```", value="Check the bot's ping.", inline=True)
        embed.add_field(name="```!start```", value="Create a ChatGPT channel.", inline=True)
        embed.add_field(name="```!stop```", value="Delete the ChatGPT channel.", inline=True)
        embed.add_field(name="```!delete [amount]```", value="Delete messages in the current channel.", inline=True)
        embed.add_field(name="```!help```", value="Show this help message.", inline=True)
        embed.add_field(name="```!poll [timer] [option1] [option2] ...```", value="Create a poll.", inline=True)

        embed.set_author(name=Bot.botName, icon_url=Bot.botProf)
        embed.set_footer(
            text=Developer.devName,
            icon_url=Developer.devProf
        )
        return embed