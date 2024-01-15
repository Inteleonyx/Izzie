import discord,os, openai, bardapi
from os import listdir
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
token_bot = os.getenv("DISCORD_TOKEN")

class Client(commands.Bot):
    def __init__(self) -> None:

        super().__init__(command_prefix='-', intents=discord.Intents().all())
        self.synced = False 
        self.cogslist = []
       
        for cog in listdir("cogs"):
            if cog.endswith(".py"):
                cog = os.path.splitext(cog)[0]
                self.cogslist.append('cogs.' + cog)

    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="MagicPacks os melhores!")) #Indica oque exibir no status do bot.
        if not self.synced:
            await self.tree.sync()
            self.synced = True
            print(f"Comandos sicronizados: {self.synced}")
        print(f"\no Bot {self.user} Já esta Online e disponivel")

client = Client()


client.run(token_bot)