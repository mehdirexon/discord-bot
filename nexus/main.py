import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from assets.chatGPTChannel import ChatGPTChannel

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help"
        )
    )

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name == "chatgpt-channel":
        if ctx.content.startswith("!"):
            await bot.process_commands(ctx)
        elif ChatGPTChannel.isUserAllowed(ctx=ctx):
            answer = ChatGPTChannel.query(ctx.content)
            await ctx.channel.send(embed=answer)
    else:
        await bot.process_commands(ctx)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed_var = discord.Embed(title="❌ Error!", color=0xff0000)
        embed_var.add_field(
            name="Details:",
            value="This command doesn't exist. Enter `!help` to get more information.\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed_var.set_footer(
            text="Nexus",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"
        )
        msg = await ctx.send(embed=embed_var)

        await ctx.message.delete(delay=5)
        await msg.delete(delay=5)


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="Ping",
        description=f":ping_pong: Pong! Latency: {latency}ms",
        color=0x0099ff
    )
    embed.set_footer(text="Nexus", 
                            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"
                    )
    message = await ctx.send(embed=embed)

    await ctx.message.delete(delay=5)
    await message.delete(delay=5)

@bot.command()
async def chatgpt(ctx):
    embed = discord.Embed(title="ChatGPT Channel", description="enter ```!start``` to create a text channel in order to chat", color=0x0099ff)

    await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
    category = discord.utils.get(ctx.guild.categories, id=1110871850206117960)
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await ctx.guild.create_text_channel(name="chatgpt-channel", category=category, overwrites=overwrites)

    welcome_message = f"Welcome to the ChatGPT channel, {ctx.author.mention}! You can start chatting with ChatGPT here."
    await channel.send(welcome_message)


@bot.command()
async def stop(ctx):
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name == "chatgpt-channel":
        await ctx.channel.delete()
    else:
        await ctx.send("This command can only be used in a ChatGPT channel.")

@bot.command()
async def delete(ctx, arg):
    if arg == "all":
        role = discord.utils.get(ctx.guild.roles, id=1110838063317405798)
        if role in ctx.author.roles:
            await ctx.channel.purge(limit=None)
        else:
            embed_var = discord.Embed(title="❌ Error!", color=0xff0000)
            embed_var.add_field(
                name="Details:",
                value="you don't have the permission to do that!\nthis message will be deleted in the next 5 seconds",
                inline=False
            )
            embed_var.set_footer(
                text="Nexus",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"
            )
            msg = await ctx.send(embed=embed_var)

            await ctx.message.delete(delay=5)
            await msg.delete(delay=5)
            
            return
    else:
        await ctx.channel.purge(limit=int(arg))


bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:", color=0x00ff00)
    embed.add_field(name="```!ping```", value="Check the bot's ping.", inline=True)
    embed.add_field(name="```!start```", value="Create a ChatGPT channel.", inline=True)
    embed.add_field(name="```!stop```", value="Delete the ChatGPT channel.", inline=True)
    embed.add_field(name="```!delete [amount]```", value="Delete messages in the current channel.", inline=True)
    embed.add_field(name="```!help```", value="Show this help message.", inline=True)
    embed.add_field(name="```!poll [timer] [option1] [option2] ...```", value="Create a poll.", inline=True)
    embed.set_footer(text="Nexus", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png")
    await ctx.channel.send(embed=embed.show_help())


@bot.command()
async def poll(ctx, timer: int, *options):
    if not 2 <= len(options) <= 10:
        embed_var = discord.Embed(title="❌ Error!", color=0xff0000)
        embed_var.add_field(
            name="Details:",
            value="Please provide between 2 and 10 options for the poll.\nthis message will be deleted in the next 5 seconds",
            inline=False
        )
        embed_var.set_footer(
            text="Nexus",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png"
        )
        msg = await ctx.send(embed=embed_var)

        await ctx.message.delete(delay=5)
        await msg.delete(delay=5)
        
        return

    number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    poll_message = "**Poll:**\n\n"
    for index, option in enumerate(options):
        poll_message += f"{number_emojis[index]} {option}\n"

    poll_embed = discord.Embed(title="📊 Poll", description=poll_message, color=0x0099ff)
    poll_embed.set_footer(text="React to vote!")

    for index in range(len(options)):
        await poll_message.add_reaction(number_emojis[index])

    timer_embed = discord.Embed(title="⏲️ Timer", description=f"Time remaining: {timer} seconds", color=0x0099ff)

    timer_message = await ctx.send(embed=timer_embed)

    for i in range(timer, 0, -1):
        timer_embed.description = f"Time remaining: {i} seconds"
        await timer_message.edit(embed=timer_embed)
        await asyncio.sleep(1)

    updated_message = await ctx.fetch_message(poll_message.id)

    max_votes = 0
    max_option = None

    for reaction in updated_message.reactions:
        if reaction.emoji in number_emojis:
            count = reaction.count - 1
            if count > max_votes:
                max_votes = count
                max_option = number_emojis.index(reaction.emoji)

    if max_option is not None:
        result_embed = discord.Embed(title="📊 Poll Result", color=0x0099ff)
        result_embed.add_field(name="Question:", value=poll_message.embeds[0].description, inline=False)
        result_embed.add_field(name="Winner:", value=options[max_option], inline=False)
        result_embed.add_field(name="Votes:", value=max_votes, inline=False)

        await ctx.send(embed=result_embed)

    await poll_message.delete()
    await timer_message.delete()


bot.run(TOKEN)