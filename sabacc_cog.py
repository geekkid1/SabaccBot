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

  @commands.command(name="setup-game",help="Start a game that people can join and then play. Also automatically adds you to the game.")
  def game_setup(self,ctx):
    self.games[ctx.channel.id] = {}
    self.games[ctx.channel.id]["players"] = []
    self.games[ctx.channel.id]["players"].add(ctx.author.id)
    self.games[ctx.channel.id]["deck"] = Deck()
    ctx.send("Game setup! Now up to five more people can join using the `join` command!")

  @commands.command(name="join-game",help="Join a game that is about to be started. Must be run in a channel where a game is being setup.")
  def game_join(self,ctx):
    try:
      if self.games[ctx.channel.id] != {}:
        pass
      else:
        ctx.send("There is no game available to join in this channel!",delete_after=5)
    except:
      ctx.send("There is no game available to join in this channel!",delete_after=5)


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
