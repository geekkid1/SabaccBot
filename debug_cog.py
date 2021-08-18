import discord
from discord.ext import commands, menus
from referral_cog import Confirm
import dbobj,os
from util_classes import database
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash import cog_ext

class debug(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.is_owner()
  @commands.command(name="repair-database",help="Create database tables (other than servers, since if that table doesn't exist, nothing will work) if they do not already exist. Add new lines to the code if you add new tables.")
  async def db_repair(self,ctx):
    database.repair_table(dbobj.servers)
