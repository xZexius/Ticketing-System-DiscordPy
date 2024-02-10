import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ui import Button, View, button
from discord import app_commands
import asyncio
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

TOKEN = "00000000000000000000000000000000000000000000000000000000"
TICKET_ROLE_ID = 0000000000000000000
CATEGORY_ID = 000000000000000000

class ButtonCompra(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @button(label="Ticket Support", style=discord.ButtonStyle.grey, emoji="🏷️", custom_id="ticket_support")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=CATEGORY_ID)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} NO CAMBIES LA BIO DE ESTE CANAL!":
                await interaction.followup.send("Ya tienes un ticket abierto en {0}".format(ch.mention), ephemeral=True)
                return
        r1 : discord.Role = interaction.guild.get_role(TICKET_ROLE_ID)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages = True)
        }
        channel = await category.create_text_channel(
            name=f"${interaction.user.name}-soporte",
            topic = f"{interaction.user.id} NO CAMBIEN ESTO!",
            overwrites=overwrites
        )
        await channel.send(
            embed=discord.Embed(
                title="Panel de soporte",
                description=f"¡Gracias por abrir ticket! Pronto un miembro del staff le atenderá.",
                color = discord.Color.green()
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/1190205794201895004/1204867428509810748/rtunetp3q3i4ca4ong3gkhi7df.png?ex=65d64b3c&is=65c3d63c&hm=24b6e169976bf58fb515e4f99006927cc3eac97b6c98dbfe31d1ca9846d24aa1&")
            .set_author(name="Zexius Development"), view = CloseButton()
        )
        await interaction.followup.send(
            embed = discord.Embed(
                description = "Tu ticket ha sido creado en: {0}".format(channel.mention),
                color = discord.Color.green()
            ), ephemeral=True
        )
        
@bot.command(name="ticket", description="Lanza el sistema de tickets.")
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    await ctx.send(
        embed=discord.Embed(
            description="Presiona el botón de abajo si necesitas soporte."
        ),
        view=ButtonCompra()
    )
    
class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @button(label="Cerrar Ticket", style=discord.ButtonStyle.red, custom_id="close", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        await interaction.channel.send("Cerrando este ticket en 3 segundos!")
        
        await asyncio.sleep(3)
        
        await interaction.channel.delete()

@tasks.loop(seconds=5)
async def update_presence():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Zexius Development 🌠"))
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ticketing System 🏷️"))

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"e")
    update_presence.start()
    bot.add_view(ButtonCompra())
    bot.add_view(CloseButton())
    
bot.run(TOKEN)