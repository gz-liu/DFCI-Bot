import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!', help_command=None)
CHARACTERS = ['Asuna', 'Asuna', 'Kirino', 'Kuroko', 'Taiga', 'Kuroyukihime', 'Mikoto', 'Miyuki',
              'Selvaria', 'Yukina', 'Shizuo', 'Tomoka', 'Emi', 'Tatsuya', 'Yuuki', 'Rentaro',
              'Kirito', 'Quenser', 'Shana', 'Ako']

@bot.event
async def on_ready():
    print("I'm up and ready :)")


@bot.command()
async def help(ctx):
    await ctx.send(""
                   "!fd {character} {move} - get frame data of character i.e. !fd Asuna 5AB"
                   "")


@bot.command(pass_context=True)
async def fd(ctx, arg1, arg2):
    character = arg1.capitalize()
    move = arg2.upper().replace('+', '')
    if iequal(move, 'ranbu'):
        move = '63214BC'
    if iequal(move, 'trump'):
        move = '5AC'
    embed = discord.Embed(title=character + ' ' + move, colour=0xa442f5)

    if character.casefold() in (name.casefold() for name in CHARACTERS):
        # use query data to scrape frame data of moves

        with open('json/{}.json'.format(arg1)) as f:
            f = json.load(f)

        for move_list in f:
            if move_list['Name'] == move:
                file = discord.File('images/{0}/{1}.png'.format(character, move), filename="image.png")
                embed.set_image(url='attachment://image.png')
                embed.add_field(name='Damage', value=move_list['Damage'])
                embed.add_field(name='Startup', value=move_list['Startup'])
                embed.add_field(name='Active', value=move_list['Active'])
                embed.add_field(name='Recovery', value=move_list['Recovery'])
                embed.add_field(name='Frame advantage', value=move_list['Frame_adv'])
                await ctx.send(file=file, embed=embed, delete_after=15)
                return
        await ctx.send("I couldn't find the move...")
    else:
        await ctx.send("I couldn't find the character/move...")


@fd.error
async def fd_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('I cannot find the character/move...')
        return


def iequal(a, b):
    try:
        return a.upper() == b.upper()
    except AttributeError:
        return a == b


bot.run(TOKEN)
