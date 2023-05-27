import discord
import asyncio
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChatGPTChannel():
    channels = [1110871391970000936,1110957540063326338]
    allowedRole = 1111764146434887680
    @staticmethod
    def isInChannel(channelID)-> bool:
        if channelID in ChatGPTChannel.channels:
            return True
        return False
    @staticmethod
    def isUserAllowed(ctx)->bool:
        role = discord.utils.get(ctx.guild.roles, id=ChatGPTChannel.allowedRole)
        if role in ctx.author.roles:
            return True
        else:
            return False    
    
    @staticmethod
    def query(input) -> discord.Embed:
        user_input = input
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        #creates a templete of the anwser for the message
        embedVar = discord.Embed(
            title=":speech_balloon: Q: " + user_input,
            color=0x00ffff
        )
        embedVar.set_footer(
            text="Nexus",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"
        )
        embedVar.add_field(
            name=":robot: Response from ChatGPT",
            value=response.choices[0].text.strip()[:1024],
            inline=False
        )
        return embedVar
        
    