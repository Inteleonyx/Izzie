import discord,os,random,asyncio,openai, io
from discord.ext import commands
from discord import app_commands,utils
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageOps

openai.api_key = "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"

afklist = [] #Lista de usuarios afk vazia para ser usada depois
      #FUNCÔES AQUII EM BAIXO

#FUNÇÂO USUARIO INFO
async def buscaruser(interaction,membro,menu):
  print (f"Usuario: {interaction.user.name} usou comando usuario")
  if membro == None:
    membro = interaction.user
  resposta = discord.Embed(
    colour=discord.Color.blue(),
    description=f"**🗄️┃Informações de {membro.name}**"
  )
  resposta.set_thumbnail(url=membro.avatar.url)
  resposta.add_field(name="🪪⠂Nome", value=f"```{membro.name}#{membro.discriminator}```", inline=True)
  resposta.add_field(name="🆔⠂ID", value=f"```{membro.id}```", inline=True)
  resposta.add_field(name="💎⠂menção", value=membro.mention, inline=True)
  resposta.add_field(name="📅⠂Entrou no servidor", value=f"```{datetime.strftime(membro.joined_at, '%d/%m/%Y às %H:%M:%S')}```", inline=True)
  resposta.add_field(name="👋⠂Entrou no discord", value=f"```{datetime.strftime(membro.created_at, '%d/%m/%Y às %H:%M:%S')}```", inline=True)
  if len(membro.roles) == 1:
    resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value="```💎⠂Sem cargos```", inline=False)
  else:
     roles_list = [role.mention for role in membro.roles if role.name != '@everyone']
     if len(roles_list) > 5:
        roles_list = roles_list[:5]  # Limita a lista aos primeiros 5 cargos
        roles_list.append("...")  # Adiciona "..." para indicar que há mais cargos
        resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value='\n • '.join(roles_list), inline=False)
     else:resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value='\n • '.join([role.mention for role in membro.roles if role.name != '@everSyone']), inline=False)
  if menu is True: #isso verifica se o comando veio do menu se sim ele manda como ephemeral
     await interaction.response.send_message(embed=resposta,ephemeral=True)
  else: await interaction.response.send_message(embed=resposta)

#Função USUARIO AVATAR
async def buscaravatar(interaction,membro,menu):
  print (f"Usuario: {interaction.user.name} usou avatar")
  if membro == None:
    membro = interaction.user
  resposta = discord.Embed(
    title="💎┃Avatar de Usuário",
    description=f"Aqui está o avatar do membro: {membro.name}",
    colour=discord.Color.blue()
  )
  resposta.set_image(url=f"{membro.avatar}")
  view = discord.ui.View()
  item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.avatar.url}")
  view.add_item(item=item)
  if menu is True: #isso verifica se o comando veio do menu se sim ele manda como ephemeral
     await interaction.response.send_message(embed=resposta,view=view,ephemeral=True)
  else: await interaction.response.send_message(embed=resposta,view=view)


#FUNÇÂO USUARIO ABRAÇAR
async def funcaoabracarusuario(interaction,membro):
  print (f"Usuario: {interaction.user.name} usou avatar")
  #o imagem é uma lista de links de imagens que serão sorteados e um será enviado
  imagem = ["https://33.media.tumblr.com/8ac1eaeaa670c65b7dbb9ceff34e4d8b/tumblr_ntdyqagJ101r8sc3ro1_r1_500.gif","https://media.tenor.com/AyIx-RCO4aQAAAAC/pokemon-hug.gif"]
  resposta = discord.Embed(
    description=f"💎┃{interaction.user.mention} abraçou {membro.mention}!",
    colour=discord.Color.blue()
  )
  resposta.set_image(url=f"{random.choice(imagem)}")
  await interaction.response.send_message(embed=resposta)
  


#INICIO DA CLASSE
class misc(commands.Cog):
  def __init__(self, client: commands.Bot) -> None:
        self.client = client
        #Carrega os menu e adiciona eles
        self.menu_useravatar = app_commands.ContextMenu(name="Usuario Avatar",callback=self.useravatarmenu)
        self.menu_userinfo = app_commands.ContextMenu(name="Usuario Info",callback=self.userinfomenu)
        self.menu_userbanner = app_commands.ContextMenu(name="Usuario Banner",callback=self.userbannermenu)
        self.menu_userabraco = app_commands.ContextMenu(name="Usuario Abraço",callback=self.userabracomenu)
        self.client.tree.add_command(self.menu_useravatar)
        self.client.tree.add_command(self.menu_userinfo)
        self.client.tree.add_command(self.menu_userbanner)
        self.client.tree.add_command(self.menu_userabraco)

  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog Misc carregado.")

  @commands.Cog.listener()
  #esse on_messagem é responsavel pelo sistema de avisos /bump e do afk dos usuarios
  async def on_message(self,message):
    #verifica todos os usuarios da lista de afk
    for i in range(len(afklist)):
      if (f"<@{afklist[i]}>" in message.content) and (not message.author.bot):
        msgenviada = await message.channel.send(f"<:BraixSleep:988776304587440148>┃ eiii {message.author.mention} quem você marcou **está afk** no momento pelo motivo: `{afklist[i+1]}`")
        await asyncio.sleep(15.0)
        await msgenviada.delete()
        return None
      break


  @commands.Cog.listener()
  #verifica todos os usuarios que digitam, se ele estiver na afklist ele desativa o afk automaticamente
  async def on_typing(self, channel, user, when):
    if user.id in afklist:
      i = afklist.index(user.id)
      afklist.remove(afklist[i+1])
      afklist.remove(user.id)
      msgenviada = await channel.send(f"💎┃ {user.mention} Seu afk foi desativado!!!")
      print(f"{user.mention} Saiu do afk")
      await asyncio.sleep(15.0)
      await msgenviada.delete()


  #Remove os menu se necessario - deixa isso aqui é importante ter
  async def cog_unload(self) -> None:
        self.client.tree.remove_command(self.menu_useravatar, type=self.menu_useravatar.type)
        self.client.tree.remove_command(self.menu_userinfo, type=self.menu_userinfo.type)
        self.client.tree.remove_command(self.menu_userbanner, type=self.menu_userbanner.type)


#GRUPO USUARIOS 
  usuario=app_commands.Group(name="usuario",description="Comandos de usuarios do bot.")

#COMANDO USUARIO AVATAR MENU
  async def useravatarmenu(self,interaction: discord.Interaction, membro: discord.Member):
    menu = True
    await buscaravatar(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO AVATAR SLASH
  @usuario.command(name="avatar",description='👤⠂Exibe o avatar de um membro')
  @app_commands.describe(membro="informe um membro")
  async def useravatar(self,interaction: discord.Integration,membro: discord.Member=None):
    menu = False
    await buscaravatar(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO INFO MENU
  async def userinfomenu(self,interaction: discord.Interaction, membro: discord.Member):
    menu = True
    await buscaruser(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO INFO SLASH
  @usuario.command(name="info",description='👤⠂Verifica as informações de um membro')
  @app_commands.describe(membro="informe um membro")
  async def userinfo(self,interaction: discord.Integration,membro: discord.Member=None):
    menu = False
    await buscaruser(interaction,membro,menu)# chama a função lá em cima
 
#COMANDO USUARIO ABRAÇO MENU
  async def userabracomenu(self,interaction: discord.Interaction, membro: discord.Member):
    await funcaoabracarusuario(interaction,membro) # chama a função lá em cima

#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="abraçar",description='👤⠂Abraçe um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    await funcaoabracarusuario(interaction,membro) # chama a função lá em cima

#COMANDO USUARIO BANNER MENU
  async def userbannermenu(self,interaction: discord.Interaction, membro: discord.Member=None):
    print (f"Usuario: {interaction.user.name} usou banner")
    if membro == None:
        membro = interaction.user
    membro = await self.client.fetch_user(membro.id)
    if membro.banner:
      resposta = discord.Embed(
        title=f"💎┃Banner de {membro.name}",
        colour=discord.Color.blue()
      )
      resposta.set_image(url=f"{membro.banner.url}")
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.banner.url}")
      view.add_item(item=item)
      await interaction.response.send_message(ephemeral=True,embed=resposta,view=view)
    else:await interaction.response.send_message(f"<:BraixBlank:969396003436380200> - Parece que o {membro.mention} não possui um banner que pena.", ephemeral=True)


#COMANDO USUARIO BANNER SLASH
  @usuario.command(name="banner",description='👤⠂Exibe o banner de um membro')
  @app_commands.describe(membro="informe um membro")
  async def userbanner(self,interaction: discord.Interaction, membro: discord.Member=None):
    print (f"Usuario: {interaction.user.name} usou banner")
    if membro == None:
        membro = interaction.user
    membro = await self.client.fetch_user(membro.id)
    if membro.banner:
      resposta = discord.Embed(
        title=f"💎┃Banner de {membro.name}",
        colour=discord.Color.blue()
      )
      resposta.set_image(url=f"{membro.banner.url}")
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.banner.url}")
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta,view=view)
    else:await interaction.response.send_message(f"<:BraixBlank:969396003436380200> - Parece que o {membro.mention} não possui um banner que pena.", ephemeral=True)

#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="atacar",description='👤⠂Ataque um membro')
  @app_commands.describe(membro="informe um alvo")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou atacar")
    resposta = discord.Embed(
      description=f"💧┃ Inteleon usou Jato d'água em {membro.mention}!",
      colour=discord.Color.blue()
    )
    resposta.set_image(url=f"https://cdn.discordapp.com/attachments/1050524867675566211/1160296885349785671/intely-inteleon.gif?ex=653425ae&is=6521b0ae&hm=c863f20d47ec7c17f82004bde3da6be59d00d3171f80086496a8f1ea5a84bac1&")
    await interaction.response.send_message(embed=resposta)
  
#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="carinho",description='👤⠂Faça carinho em um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou carinho")
    resposta = discord.Embed(
      description=f"💎┃{interaction.user.mention} fez carinho em {membro.mention}!",
      colour=discord.Color.blue()
    )
    resposta.set_image(url=f"https://i.makeagif.com/media/6-13-2015/5aAShu.gif")
    await interaction.response.send_message(embed=resposta)

#COMANDO USUARIO CAFUNÉ SLASH
  @usuario.command(name="cafuné",description='👤⠂Faça cafuné em um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou cafuné")
    resposta = discord.Embed(
      description=f"💎┃{interaction.user.mention} fez cafuné em {membro.mention}!",
      colour=discord.Color.blue()
    )
    resposta.set_image(url=f"https://cdn.discordapp.com/attachments/1067789510097768528/1139147429367791696/Braixen_carinho.gif")
    await interaction.response.send_message(embed=resposta)


#COMANDO USUARIO AFK
  @usuario.command(name="afk",description='👤⠂fique afk')
  @app_commands.describe(motivo="informe um membro")
  async def userafk(self,interaction: discord.Integration,motivo: str=None):
    print (f"Usuario: {interaction.user.name} usou afk")
    if motivo == None:
      motivo = "Ele não falou"
    afklist.append(interaction.user.id)
    afklist.append(motivo)
    resposta = discord.Embed(
      description=f"💎┃Você agora está afk!",
      colour=discord.Color.blue()
    )
    await interaction.response.send_message(embed=resposta,ephemeral=True)


#GRUPO SERVIDOR 
  servidor=app_commands.Group(name="servidor",description="Comandos de usuarios do bot.")

#COMANDO ICONE DE SERVIDOR
  @servidor.command(name="icone", description='🗄️⠂Exibe o ícone do servidor')
  async def icone(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou icone do servidor")
    servidor = interaction.guild
    icone_url = servidor.icon.url if servidor.icon else None
    if icone_url:
      resposta = discord.Embed(
        title="💎┃Ícone do Servidor",
        description=f"Aqui está o ícone do servidor: {servidor.name}",
        colour=discord.Color.blue()
      )
      resposta.set_image(url=icone_url)
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=icone_url)
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta, view=view)
    else:
      await interaction.response.send_message("❌┃ O servidor não possui ícone.", ephemeral=True)


#COMANDO BANNER DE SERVIDOR
  @servidor.command(name="banner", description='🗄️⠂Exibe o banner do servidor')
  async def banner(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou banner do servidor")
    servidor = interaction.guild
    banner_url = servidor.banner.url if servidor.banner else None
    if banner_url:
      resposta = discord.Embed(
        title="💎┃Banner do Servidor",
        description=f"Aqui está o banner do servidor: {servidor.name}",
        colour=discord.Color.blue()
      )
      resposta.set_image(url=banner_url)
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=banner_url)
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta, view=view)
    else:
      await interaction.response.send_message("❌┃ O servidor não possui um banner.", ephemeral=True)
    

#COMANDO SPLASH DE SERVIDOR
  @servidor.command(name="splash", description='🗄️⠂Exibe a splash do servidor')
  async def splash(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou splash do servidor")
    servidor = interaction.guild
    splash_id = servidor.splash
    if splash_id:
        splash_url = f"{splash_id}"
        resposta = discord.Embed(
            title="💎┃Splash do Servidor",
            description="Aqui está a splash do servidor:",
            colour=discord.Color.blue()
        )
        resposta.set_image(url=splash_url)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=splash_url)
        view.add_item(item=item)
        await interaction.response.send_message(embed=resposta, view=view)
    else:
        await interaction.response.send_message("❌┃ O servidor não possui uma splash definida.", ephemeral=True)
  

#COMANDO INFORMAÇÂO DE SERVIDOR
  @servidor.command(name="info", description='🗄️⠂Exibe informações sobre o servidor')
  @app_commands.describe(id="informe uma id de um servidor")
  async def infoservidor(self, interaction: discord.Interaction, id: str=None):
    print(f"Usuario: {interaction.user.name} usou infoservidor")
    if id is None:
      servidor = interaction.guild
    else:
      servidor = self.client.get_guild(int(id))
      if servidor is None:
        await interaction.response.send_message("❌┃ Não achei esse servidor.", ephemeral=True)
        return
    icone_url = servidor.icon.url if servidor.icon else None
    resposta = discord.Embed(
        title=f"💎┃Informações de {servidor.name}",
        description=servidor.description,
        colour=discord.Color.blue()
    )
    resposta.set_thumbnail(url=icone_url)
    resposta.add_field(name="<:user:1054410113743597671> Usuarios", value=f"```Total: {servidor.member_count}\nPessoas: {sum(1 for member in servidor.members if not member.bot)}\nBots: {sum(1 for member in servidor.members if member.bot)}```")
    resposta.add_field(name=":file_folder: Canais", value=f"```Total: {len(servidor.channels)}\nTexto: {sum(1 for canal in servidor.channels if isinstance(canal, discord.TextChannel))}\nVoz: {sum(1 for canal in servidor.channels if isinstance(canal, discord.VoiceChannel))}```")
    resposta.add_field(name="<:Crown:992470407082934382> Dono", value=f"```{servidor.owner.name}\n{servidor.owner.id}```")
    resposta.add_field(name="<:Id:1059244242440032357> ID", value=f"```{servidor.id}```")
    resposta.add_field(name="<:IconCalendar:1045880078615199795> Criado em", value=f"```{servidor.created_at.strftime('%d/%m/%Y às %H:%M:%S')}```")
    resposta.add_field(name="🍰 Emojis", value=f"```Total: {len(servidor.emojis)}```")
    await interaction.response.send_message(embed=resposta)

jogos=app_commands.Group(name="jogos",description="Comandos de jogos da Izzie")

@jogos.command(name = 'ship', description='Cheque se alguém é sua alma gêmea')
@app_commands.describe(
    usuario1 = "Primeiro usuário a shippar",
    usuario2 = "Segundo usuário a shippar",
)
async def ship(interaction: discord.Interaction,usuario1: discord.User or discord.User.id,usuario2: discord.User or discord.User.id):
    print(f"{interaction.user} No servidor {interaction.guild}")
    porcentagem = random.randint(0,100)
    metade1 = usuario1.name[:len(usuario1.name)//2]
    metade2 = usuario2.name[len(usuario2.name)//2:]
    nomeship = metade1 + metade2

    imagem1 = await usuario1.avatar.read()
    avatar1 = Image.open(io.BytesIO(imagem1))
    avatar1 = avatar1.resize((250,250))

    imagem2 = await usuario2.avatar.read()
    avatar2 = Image.open(io.BytesIO(imagem2))
    avatar2 = avatar2.resize((250,250))

    planodefundo = Image.new("RGB",(500,280),(56,56,56))
    planodefundo.paste(avatar1,(0,0))
    planodefundo.paste(avatar2,(250,0))

    fundodraw = ImageDraw.Draw(planodefundo)
    fundodraw.rounded_rectangle(((0,250),(500*(porcentagem/100),289)),fill=(207, 13, 48),radius=5)

    fonte = ImageFont.truetype("RobotoMono-Bold.ttf",20)
    fundodraw.text((230,250),f"{porcentagem}%",font=fonte)

    buffer = io.BytesIO()
    planodefundo.save(buffer,format="PNG")
    buffer.seek(0)

    if porcentagem <= 35:
        mensagem_extra = "😅 Não parece rolar uma química tão grande, mas quem sabe...?"
    elif porcentagem <= 45:
        mensagem_extra = "😄 Essa combinação tem potencial, que tal um jantar romântico?"
    elif porcentagem <= 65:
        mensagem_extra = "😘 Quem Sabe...?" 
    elif porcentagem <= 85:
        mensagem_extra = "🤨 Talvez funcione, mas precisa trabalhar."
    elif porcentagem <= 90:
        mensagem_extra = "😍 Casal perfeito, quando será o casamento?"
    elif porcentagem <= 99:
        mensagem_extra = "🥰 Casal inseparavel"
    else:
        mensagem_extra = "☠️ Nem a Dona morte se para."

    await interaction.response.send_message(f"❤️ **Será que vamos ter um casal novo por aqui?** 🧡\n {usuario1.mention} + {usuario2.mention} = ✨ `{nomeship}` ✨\n{mensagem_extra}",file=discord.File(fp=buffer,filename="file.png"))


async def setup(client:commands.Bot) -> None:
  await client.add_cog(misc(client))