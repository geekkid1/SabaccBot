import discord
from discord.ext import commands,menus
from referral_cog import Confirm
import dbobj,os
from util_classes import database
import random

class sabacc(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.games = {}

  @commands.command(name="setup-account")
  async def acct_setup(self,ctx):
    acct = database.select_one(dbobj.accounts, id=ctx.author.id)
    if acct == [] or acct == None:
      database.insert_row(dbobj.accounts, (ctx.author.id,100))
      await ctx.send("Your account has been initialized to 100 credits. If you want more, plead with a moderator about it I guess. See what happens.")
    else:
      await ctx.send("You may already have an account. If you believe this to be untrue, check with the owner of the bot or a moderator.")

  @commands.command(name="setup-game",help="Start a game that people can join and then play. Also automatically adds you to the game.")
  async def game_setup(self,ctx):
    acct = database.select_one(dbobj.accounts, id=ctx.author.id)
    if acct == [] or acct[1] == 0:
      await ctx.send("You have no credits! If this is because you do not have an account, make one with the `create-account` command. If this is because you have bad luck... maybe ask a moderator if you can have a bit more money?",delete_after=7)
      return
    try:
      if self.games[ctx.channel.id] != {}:
        await ctx.send("There is either already a game running here in this channel, or the bot is broken. Sorry if it's the latter.",delete_after=5)
    except:
      pass
    self.games[ctx.channel.id] = {}
    self.games[ctx.channel.id]["players"] = []
    self.games[ctx.channel.id]["players"].add(ctx.author.id)
    self.games[ctx.channel.id]["deck"] = Deck()
    msg = await ctx.send("Game setup complete! Now up to five more people can join using the `join-game` command! (1/6 Players Joined)")
    self.games[ctx.channel.id]["msg"] = msg.id

  @commands.command(name="join-game",help="Join a game that is about to be started. Must be run in a channel where a game is being setup.")
  async def game_join(self,ctx):
    try:
      if self.games[ctx.channel.id] != {}:
        acct = database.select_one(dbobj.accounts, id=ctx.author.id)
        if acct == [] or acct[1] == 0:
          await ctx.send("You have no credits! If this is because you do not have an account, make one with the `create-account` command. If this is because you have bad luck... maybe ask a moderator if you can have a bit more money?",delete_after=7)
          return
        if len(self.games[ctx.channel.id]["players"]) >= 6:
          await ctx.send("Sorry, this game is full at the moment.",delete_after=5)
          return
        self.games[ctx.channel.id]["players"].add(ctx.author.id)
        await ctx.send("You were successfully added to the game!",delete_after=5)
        msg = await ctx.channel.fetch_message(self.games[ctx.channel.id]["msg"])
        await msg.edit("Game setup complete! Now up to five more people can join using the `join-game` command! ({0}/6 Players Joined)".format(len(self.games[ctx.channel.id]["players"])))
      else:
        await ctx.send("There is no game available to join in this channel!",delete_after=5)
    except:
      await ctx.send("There is no game available to join in this channel!",delete_after=5)


class Card():
  def __init__(self,name,value):
    self.name = name
    self.value = value

class Deck():
  def __init__(self):
    self.contents = []
    suits = ["Circles","Squares","Triangles"]
    for suit in suits:
      for x in range(1,10):
        self.contents.add(Card(str(x) + " of " + suit, x))
      for x in range(-10,-1):
        self.contents.add(Card(str(x) + " of " + suit, x))

    self.contents.add(Card("Zero",0))
    self.contents.add(Card("Zero",0))

  def draw(self):
    r_index = random.randint(0,len(self.contents))
    r = self.contents[r_index]
    self.contents.remove(r)
    return r