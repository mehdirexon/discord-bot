import discord
import openai
from config import OPENAI_API_KEY
from profiles import Bot
openai.api_key = OPENAI_API_KEY

class ChatGPTChannel():
    allowedRole = 1111764146434887680 #change it for your own role

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
        embed = discord.Embed(
            title=":speech_balloon: Q: " + user_input,
            color=0x00ffff
        )
        embed.set_author(name="chatGPT", icon_url="https://uploads-ssl.webflow.com/5b105a0c66f2f636c7884a17/64063dbcad97bd421b437096_chatgpt.jpg")
        embed.set_footer(
            text=Bot.botName,
            icon_url=Bot.botProf
        )
        
        embed.add_field(
            name=":robot: Response from ChatGPT",
            value=response.choices[0].text.strip()[:1024],
            inline=False
        )
        return embed
        
    