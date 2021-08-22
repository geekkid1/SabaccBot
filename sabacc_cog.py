import discord
from discord.ext import commands,menus
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
    self.games[ctx.channel.id]["players"].append(ctx.author.id)
    self.games[ctx.channel.id]["host"] = ctx.author.id
    self.games[ctx.channel.id]["status"] = "Preparing"
    self.games[ctx.channel.id]["hands"] = {}
    self.games[ctx.channel.id]["hands"][ctx.author.id] = []
    self.games[ctx.channel.id]["deck"] = Deck()
    self.games[ctx.channel.id]["turn"] = 0
    msg = await ctx.send("Game setup complete! Now up to five more people can join using the `join-game` command! (1/6 Players Joined)")
    self.games[ctx.channel.id]["msg"] = msg.id

  @commands.command(name="join-game",help="Join a game that is setup and about to be started. Must be run in a channel where a game is being setup.")
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
        if self.games[ctx.channel.id]["status"] != "Preparing":
          await ctx.send("The game is currently not joinable at the moment. Wait for another game in this channel or start a different one in another channel.",delete_after=5)
        if ctx.author.id in self.games[ctx.channel.id]["players"]:
          await ctx.send("You have already joined this game.",delete_after=5)
          return
        self.games[ctx.channel.id]["players"].append(ctx.author.id)
        self.games[ctx.channel.id]["hands"][ctx.author.id] = []
        await ctx.send("You were successfully added to the game!",delete_after=5)
        msg = await ctx.channel.fetch_message(self.games[ctx.channel.id]["msg"])
        await msg.edit("Game setup complete! Now up to five more people can join using the `join-game` command! ({0}/6 Players Joined)".format(len(self.games[ctx.channel.id]["players"])))
      else:
        await ctx.send("There is no game available to join in this channel!",delete_after=5)
    except:
      await ctx.send("There is no game available to join in this channel!",delete_after=5)

  @commands.command(name="start-game",help="Start a game that you started setting up.")
  async def game_start(self,ctx):
    try:
      if self.games[ctx.channel.id]["host"] != ctx.author.id:
        await ctx.send("You are not the host of this game. If the game is ready to start, ask them to get things started.",delete_after=5)
        return
      if len(self.games[ctx.channel.id]["players"]) <= 1:
        await ctx.send("There are not enough players to start a game! Get more people to join and then we can get started.",delete_after=5)
        return
      if self.games[ctx.channel.id]["status"] != "Preparing":
        await ctx.send("The game is not able to be started right now. If that means that the game is already running, perhaps go play.",delete_after=5)
      self.games[ctx.channel.id]["status"] = "Building"
      for p in self.games[ctx.channel.id]["players"]:
        for x in range(2):
          self.games[ctx.channel.id]["hands"][p].append(self.games[ctx.channel.id]["deck"].draw())
        c1 = self.games[ctx.channel.id]["hands"][p][0]
        c2 = self.games[ctx.channel.id]["hands"][p][1]
        sum = c1.value + c2.value
        user = await bot.fetch_user(p)
        if user.dm_channel == None:
          ch = await user.create_dm()
        else:
          ch = user.dm_channel
        await ch.send("Your starting hand is:\n1. **{0.name}**\n2.**{1.name}**\nThe sum of your hand is {2}.".format(c1,c2,sum))
      first_player = bot.fetch_user(self.games[ctx.channel.id]["players"][0])
      await ctx.send("The game has begun! All players' starting hands have been sent to them, and it is now " + first_player.mention +"'s turn! You may take a turn using the `action` command!")
    except:
      await ctx.send("Could not verify stored game data.",delete_after=5)

  @commands.command(name="action",help="Take an action on your turn in a game.")
  async def game_action(self,ctx,action):
    trn = self.games[ctx.channel.id]["turn"]
    if ctx.author.id != self.games[ctx.channel.id]["players"][trn]:
      await ctx.send("It's not your turn!",delete_after=5)
      return

class Card():
  def __init__(self,name,value):
    self.name = name
    self.value = value

  def __eq__(self,other):
    return other.value == self.value

  def __ne__(self,other):
    return other.value != self.value

  def __add__(self,other):
    try:
      return other.value + self.value
    except:
      return other + self.value

class Deck():
  def __init__(self):
    self.contents = []
    suits = ["Circles","Squares","Triangles"]
    for suit in suits:
      for x in range(1,10):
        self.contents.append(Card(str(x) + " of " + suit, x))
      for x in range(-10,-1):
        self.contents.append(Card(str(x) + " of " + suit, x))

    self.contents.append(Card("Zero",0))
    self.contents.append(Card("Zero",0))

  def draw(self):
    r_index = random.randint(0,len(self.contents))
    r = self.contents[r_index]
    self.contents.remove(r)
    return r
