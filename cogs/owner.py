import discord,os,requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

def getdonoid():
    return donoid
def getmensagemerro():
    return mensagemerro

#CARREGA E LE O ARQUIVO .env na raiz
load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
donoid = int(os.getenv("DONO_ID")) #acessa e define o id do dono
square_token = os.getenv("square_token") #acessa e define o token da square cloud
square_idaplication = os.getenv("square_idaplication") #acessa e define o id do bot na square cloud

#Mensagem de erro que será exibida sempre que um comando falhar, edite aqui e alterará tudo
mensagemerro = "<:ew:969703224825225266> Ue? Isso não funcionou como deveria... \nAcho que você tentou usar isso em um canal errado ou não tem permissão para tal função <:derp:969703169670131812>"

#inicio dessa classe
class owner(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  #usando o listener para permitir que os async daqui sejam escutados pelo main.py
  @commands.Cog.listener()
  #olha o mesmo on_ready aqui para imprimir o carregamento da cog
  async def on_ready(self):
    print("Cog onwer carregado.")

  #GRUPO SERVIDOR - aqui estou criando um grupo de comandos
  dono = app_commands.Group(name="onwer",description="Comandos de dono do bot.")

  #COMANDO SAY - neste caso estou criando um comando dentro de um grupo
  @dono.command(name="say", description="💎⠂Diga alguma coisa como Izzie")
  @app_commands.describe(mensagem="Qual é a mensagem?") #descrição adicional
  async def say(self,interaction: discord.Interaction, mensagem: str):
    print(f"Comando say - User: {interaction.user.name} - mensagem:{mensagem}") # imprime no terminal, vai ter de monte desses
    if interaction.user.id == donoid: # Verifica se o usuário é o dono do bot
      await interaction.response.send_message("🍰 ┃ enviando sua mensagem...", ephemeral=True) # Envia uma resposta de interação que só é visível para o usuário
      await interaction.channel.send(f"{mensagem}") # Envia a mensagem no canal
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True) # Envia uma resposta de erro que só é visível para o usuário

  #COMANDO LISTAR SERVIDORES
  @dono.command(name="listar", description="💎⠂lista os servidores que o Izzie está.")
  async def listservers (self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou lista servidores")
    if interaction.user.id == donoid: # Verifica se o usuário é o dono do bot
      await interaction.response.defer () # Envia uma resposta de interação para indicar que o comando está sendo processado
      servers = self.client.guilds
      lista = "Lista de Servidores 💎\n" # Cria uma variável para armazenar a lista de servidores
      for server in servers:
        lista += f"Nome:`{server.name}` - id:`{server.id}`\n" # Adiciona o nome e o id de cada servidor à lista, separados por uma quebra de linha
      await interaction.followup.send(content=lista) # Edita a resposta de interação com a lista de servidores
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True) # Envia uma resposta de interação que só é visível para o usuário

  #COMANDO SAIR Servidor
  @dono.command(name="sair", description="💎⠂Faz o Izzie sair de servidor.")
  @app_commands.describe(id_servidor="Qual é a Id do servidor?")
  async def leave (self,interaction: discord.Interaction,id_servidor:str):
    print (f"Usuario: {interaction.user.name} usou sair servidores")
    if interaction.user.id == donoid:
        guild = self.client.get_guild (int (id_servidor)) # Obtém o objeto guilda pelo ID
        await guild.leave () # Faz o bot sair da guilda
        await interaction.response.send_message(f"sai do {guild.name}")
    else:
        await interaction.response.send_message(mensagemerro,ephemeral=True)


  #COMANDO ALTERAR NOME BOT
  @dono.command(name="bot-name", description="💎⠂Define um novo nome ao bot")
  @app_commands.describe(nome="Qual é o novo nome?")
  async def say(self,interaction: discord.Interaction, nome: str):
    print(f"Comando bot-name - User: {interaction.user.name} - mensagem:{nome}")
    if interaction.user.id == donoid:
      await self.client.user.edit(username=nome) #Edita o nome de usuario do bot
      await interaction.response.send_message(f"<:BN:416595378956271626>┃ O Nome do bot definido para {nome}", ephemeral=True)
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)


  #COMANDO ALTERAR AVATAR BOT
  @dono.command(name="bot-avatar", description="💎⠂Define um novo avatar ao bot")
  @app_commands.describe(avatar="Qual é o novo avatar?")
  async def say(self,interaction: discord.Interaction, avatar: discord.Attachment):
    print(f"Comando bot-avatar - User: {interaction.user.name}")
    if interaction.user.id == donoid:
      avatar = await avatar.read()
      await self.client.user.edit(avatar=avatar) #Edita o avatar do bot
      await interaction.response.send_message(f"<:BN:416595378956271626>┃ O Avatar do bot foi redefinido", ephemeral=True)
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)




    #GRUPO BOT 
  bot=app_commands.Group(name="bot",description="Comandos de controle do bot.")
  #COMANDO PING
  @bot.command(name="ping",description='🤖⠂Exibe o ping do bot')
  async def ping(self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou ping")
    resposta = discord.Embed(
            colour=discord.Color.blue(),
            title="🏓┃Pong",
            description=f"Latencia: `{round(self.client.latency * 1000)}`ms."
        )
    await interaction.response.send_message(embed=resposta)


                  #COMANDO INFO BOT
  @bot.command(name="info",description='🤖⠂Exibe informações sobre o bot')
  async def botinfo(self, interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou botinfo")
    res_information =  requests.get(f"https://api.squarecloud.app/v2/apps/{square_idaplication}", headers={"Authorization": square_token})
    res_information = res_information.json()
    res_status =  requests.get(f"https://api.squarecloud.app/v2/apps/{square_idaplication}/status", headers={"Authorization": square_token})
    res_status = res_status.json()
    resposta = discord.Embed(
            colour=discord.Color.blue(),
            title=f"💎┃Informações do {self.client.user.name}",
            description=f"{res_information['response']['app']['desc']}"
        )
    if self.client.user.avatar:
      resposta.set_thumbnail(url=f"{self.client.user.avatar.url}")
    resposta.add_field(name="🖥️⠂squarecloud.app", value=f"```{res_information['response']['app']['cluster']}```", inline=True)
    resposta.add_field(name="👨‍💻⠂Linguagem", value=f"```{res_information['response']['app']['language']}```", inline=True)
    resposta.add_field(name="💎⠂Dono", value=f"<@{donoid}>", inline=True)
    resposta.add_field(name="📊⠂Ram", value=f"```{(res_status['response']['ram'])} / {res_information['response']['app']['ram']} MB```", inline=True)
    resposta.add_field(name="🌡⠂CPU", value=f"```{res_status['response']['cpu']}```", inline=True)
    resposta.add_field(name="🕐⠂Uptime", value=f"<t:{round(res_status['response']['uptime']/1000)}:R>", inline=True)
    resposta.add_field(name="🌐⠂Rede", value=f"```{res_status['response']['network']['total']}```", inline=True)
    resposta.add_field(name="🏓⠂Ping", value=f"```{round(self.client.latency * 1000)}ms```", inline=True)
    resposta.add_field(name="🔮⠂Menção", value=f"<@{self.client.user.id}>", inline=True)

    await interaction.response.send_message(embed=resposta)


  #help comando
  @bot.command(name="help",description='🤖⠂Ajuda sobre o bot.')
  async def help(self,interaction: discord.Integration):
    resposta = discord.Embed( 
      colour=discord.Color.blue(),
      title="💎┃Ajuda sobre o bot",
      description="Eaeee Inteleon, aqui bem eu deixei esse comando aqui para que você pudesse editar minha mensagem no onwer.py, espero que esteja gostando do bot, qualquer coisa me procure em https://dsc.gg/braixen"
    )
    await interaction.response.send_message(embed=resposta)

  @bot.command(name="avaliar",description='Avalie seu atendimento na nossa comunidade.')
  @app_commands.describe(staff="informe um membro da staff para avaliar",nota="selecione uma nota para o staff",comentario="escreva um comentario adicional.")
  @app_commands.choices(nota=[app_commands.Choice(name="1", value="1"),app_commands.Choice(name="2", value="2"),app_commands.Choice(name="3", value="3"),app_commands.Choice(name="4", value="4"),app_commands.Choice(name="5", value="5"),])
  async def avaliar(self,interaction: discord.Interaction,staff: discord.Member, nota:app_commands.Choice[str],comentario:str):
        print (f"Usuario: {interaction.user.name} usou avaliar atendimento")
        canal_avaliacao = interaction.guild.get_channel(1050524867675566211)
        if (nota.value == '1'):
            estrelas = "⭐"
        elif (nota.value == '2'):
            estrelas = "⭐⭐"
        elif (nota.value == '3'):
            estrelas = "⭐⭐⭐"
        elif (nota.value == '4'):
            estrelas = "⭐⭐⭐⭐"
        elif (nota.value == '5'):
            estrelas = "⭐⭐⭐⭐⭐"
    
        resposta = discord.Embed(
                colour=discord.Color.blue()
            )
        resposta.set_thumbnail(url=staff.avatar.url)
        resposta.add_field(name="```💎``` Staff", value=f"```{staff.name}#{staff.discriminator}```", inline=True)
        resposta.add_field(name="```⭐``` Nota", value=f"```{estrelas}```", inline=True)
        resposta.add_field(name="```🗨️``` Comentário", value=f"```{comentario}```", inline=False)
        resposta.set_footer(text=f"avaliação enviada por {interaction.user.name}#{interaction.user.discriminator}")
        await canal_avaliacao.send(embed=resposta)
        await interaction.response.send_message("Recebemos sua avaliação ebaaa :face_holding_back_tears: muito obrigado viu",ephemeral=True)

  @bot.command(name="say", description="Diga alguma coisa como Izzie")
  @app_commands.describe(mensagem="Qual é a mensagem?") #descrição adicional
  async def say(self,interaction: discord.Interaction, mensagem: str):
    print(f"Comando say - User: {interaction.user.name} - mensagem:{mensagem}") # imprime no terminal, vai ter de monte desses
    await interaction.response.send_message("🍰 ┃ enviando sua mensagem...", ephemeral=True) # Envia uma resposta de interação que só é visível para o usuário
    await interaction.channel.send(f"{mensagem}\n\n- by: {interaction.user.mention}") # Envia a mensagem no canal

async def setup(client:commands.Bot) -> None:
  await client.add_cog(owner(client))