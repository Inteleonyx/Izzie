import discord,os,asyncio,random
from discord.ext import commands
from discord import app_commands
from characterai import PyAsyncCAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
char_id = os.getenv('char_id')
char_token = os.getenv('char_token')

errobard = "**Ahh não** :sob:\nA api do bard não me respondeu, tente novamente mais tarde. <:braix:969703106818498611>"

async def enviar_mensagem_para_character_ai(self,mensagem):
  try:
    char = char_id  # Use o ID da IA globalmente definido
    chat = await self.client.chat.get_chat(char)  # Aguarde a resposta de forma assíncrona
    participants = chat['participants']
    autor = mensagem.author
    message = mensagem.content.replace("<@1159919745802449018>", "")
    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']
    mensagem = f"{autor}\n{message}"
    data = await self.client.chat.send_message(chat['external_id'], tgt, mensagem)  # Aguarde a resposta de forma assíncrona
    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']
    return f"{text}"
  except Exception as e:
    return f":sob:┃ A api do Character.ai não me respondeu...\nErro: {e}"

async def reset_character_ai(self):
  try:
    izzie = await self.client.chat.new_chat(char_id)
    text = izzie['messages'][0]['text']
    return f"{text}"
  except:
    return ":sob:┃ A api do Character.ai não me respondeu..."

class caracterai(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.client = PyAsyncCAI(char_token)
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog characterai carregado.")
  
  @commands.Cog.listener()
  async def on_message(self,message):
    #if message.author == self.client.user or message.author.bot:
    #  return
    if "<@1159919745802449018>" in message.content and message.author != self.client.user:
      async with message.channel.typing():
            await message.add_reaction('👀')
            response = await enviar_mensagem_para_character_ai(self,message)
            chance_de_aparecer = 20
            if random.randint(1, 100) <= chance_de_aparecer:
                response += "\n*<3*"
            await message.reply(response)

#GRUPO DE COMANDOS DE IMAGENS BOT 
  ai=app_commands.Group(name="ai",description="Comandos de character ai integrados no bot.")

#COMANDO CHARACTER AI RESET
  @ai.command(name="reset",description='🤖⠂resete sua conversa com Izzie.')
  async def resetcharacter(self,interaction: discord.Interaction):
    izzie = await reset_character_ai(self)
    await interaction.response.send_message("Conversa com Izzie resetada.", ephemeral=True)
    await interaction.channel.send(f"{izzie}")

#COMANDO CHARACTER AI AJUDA
  @ai.command(name="help",description='🤖⠂receba ajuda sobre CharacterAi.')
  async def helpcharacter(self,interaction: discord.Integration):
    resposta = discord.Embed(
      colour=discord.Color.blue(),
      title="💎┃ Izzie AI",
      description="Oii, sabia que eu agora tenho um chatbot completo graças a Character.ai, tenta conversar comigo agora mesmo me marcando em toda mensagem e eu tentarei te responder <3"
    )
    resposta.set_footer(text="gerado por Character.ai")
    await interaction.response.send_message(embed=resposta)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(caracterai(client))