import discord
from discord.ext import commands
import asyncio
from config import TOKEN
from chatGPTChannel import ChatGPTChannel
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
from profiles import Developer,Bot,Channels,Roles
from embed import EmbedsCreator

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

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

    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name == "chatgpt-channel": #you can change the channel name to whatever you want
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
        embed = EmbedsCreator.errorEmbed(EmbedsCreator.descriptions['commandDoesntExists'])

        msg = await ctx.send(embed=embed)

        await ctx.message.delete(delay=5)
        await msg.delete(delay=5)

@bot.command()
@cooldown(1, 3600, BucketType.user)
async def bug(ctx, *, bug_report=None):
    if ctx.channel.id != 1112820768867373066: #change it for your own server
        return

    if bug_report is None:
        embed = EmbedsCreator.emptyBugReport()
        msg = await ctx.send(embed=embed)

        await ctx.message.delete(delay=5)
        await msg.delete(delay=5)
        return
    
    #sends to the dev
    user = await bot.fetch_user(Developer.devID)
    dm_channel = await user.create_dm()

    reporter = ctx.author
    reporter_info = f"Reporter: {reporter.mention} (ID: {reporter.id})"

    embed = EmbedsCreator.reportForDev(reporter_info,bug_report)

    await dm_channel.send(embed=embed)

    await ctx.message.delete()

    embed = EmbedsCreator.showTheReport(reporter,bug_report)

    await ctx.send(embed=embed)

@bug.error
async def bug_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        cooldown_seconds = error.retry_after
        minutes, seconds = divmod(cooldown_seconds, 60)

        embed = EmbedsCreator.errorForEmbedLimitation(minutes,seconds)
        msg = await ctx.send(embed=embed)
        msg.delete(delay = 5)
    else:
        embed = EmbedsCreator.errorEmbed()
        msg = await ctx.send(embed=embed)
        msg.delete(delay = 5)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)

    embed = EmbedsCreator.pingEmbed(latency)

    message = await ctx.send(embed=embed)

    await ctx.message.delete(delay=5)
    await message.delete(delay=5)

@bot.command()
async def chatgpt(ctx):
    embed = EmbedsCreator.chatGPT()

    msg = await ctx.send(embed=embed)
    msg.delete(delay = 5)

@bot.command()
async def start(ctx):
    if ctx.channel.id != 1110957679595245678: #change it for your own server
        return
    category = discord.utils.get(ctx.guild.categories, id=Channels.chatGPTallowdCategoryID)
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await ctx.guild.create_text_channel(name="chatgpt-channel", category=category, overwrites=overwrites)

    welcome_message = f"Welcome to the ChatGPT channel, {ctx.author.mention}! You can start chatting with ChatGPT here."
    await channel.send(welcome_message)
    await ctx.message.delete()

@bot.command()
async def stop(ctx):
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name == "chatgpt-channel":
        await ctx.channel.delete()
    else:
        embed = EmbedsCreator.errorEmbed("This command can only be used in a ChatGPT channel.")
        msg = await ctx.send(embed=embed)
        await msg.delete(delay = 5)
        await ctx.message.delete(delay = 5)

@bot.command()
async def delete(ctx, arg):
    role = discord.utils.get(ctx.guild.roles, id=Roles.manager)
    if role in ctx.author.roles:
        if arg == "all":
            await ctx.channel.purge(limit=None)
        else:
            await ctx.channel.purge(limit=int(arg))
    else:
        embed = EmbedsCreator.noPermission()

        msg = await ctx.send(embed=embed)

        await ctx.message.delete(delay=5)
        await msg.delete(delay=5)
        
        return
    
@bot.command()
async def help(ctx):
    embed = EmbedsCreator.help()
    await ctx.channel.send(embed=embed)

@bot.command()
async def poll(ctx, timer: int, *options):
    if not 2 <= len(options) <= 10:
        embed_var = EmbedsCreator.errorEmbed("Please provide between 2 and 10 options for the poll.")
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

    poll_msg = await ctx.send(embed=poll_embed)

    for index in range(len(options)):
        await poll_msg.add_reaction(number_emojis[index])

    timer_embed = discord.Embed(title="⏲️ Timer", description=f"Time remaining: {timer} seconds", color=0x0099ff)

    timer_msg = await ctx.send(embed=timer_embed)

    for i in range(timer, 0, -1):
        timer_embed.description = f"Time remaining: {i} seconds"
        await timer_msg.edit(embed=timer_embed)
        await asyncio.sleep(1)

    await asyncio.sleep(1)

    updated_message = await ctx.fetch_message(poll_msg.id)

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
        result_embed.add_field(name="Question:", value=poll_embed.description, inline=False)
        result_embed.add_field(name="Winner:", value=options[max_option], inline=False)
        result_embed.add_field(name="Votes:", value=max_votes, inline=False)

        await ctx.send(embed=result_embed)
    elif max_votes == 0:
        result_embed = discord.Embed(title="📊 Poll Result", color=0x0099ff)
        result_embed.add_field(name="Question:", value=poll_embed.description, inline=False)
        result_embed.add_field(name="Winner:", value="nobody voted!", inline=False)

        msg = await ctx.send(embed=result_embed)

        await msg.delete(delay = 5)
    else:
        await ctx.send("All votes were the same. Nobody won.")

    await ctx.message.delete()
    await poll_msg.delete()
    await timer_msg.delete()

bot.run(TOKEN)