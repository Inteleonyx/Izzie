import discord,os,asyncio,random,json
from discord.ext import commands
from discord import app_commands
from characterai import PyAsyncCAI
from dotenv import load_dotenv
from config.user_data import userdata
from config.user_data import collection

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
char_id = os.getenv('char_id')
char_token = os.getenv('char_token')

print()

class fun(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog fun carregado.")

  @app_commands.command(name="saldo", description="veja o saldo de algum membro")
  async def _saldo(interaction: discord.Interaction, membro=discord.Member or discord.Member.id):
    if membro == None:
      membro = interaction.user
    user = userdata.openaccount(id=membro.id)
    saldo = collection.find_one({"saldo", 0})
    await interaction.response.send_message(f"Seu saldo é de {saldo}")
    return saldo

async def setup(client:commands.Bot) -> None:
  await client.add_cog(fun(client))