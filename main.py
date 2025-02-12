import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PRIVATE_SERVER_INVITE = os.getenv("PRIVATE_SERVER_INVITE")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable server members intent
bot = commands.Bot(command_prefix="!", intents=intents)

WHITELIST_FILE = "whitelist.json"

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    return {}
def save_whitelist(data):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(data, f, indent=4)
whitelist = load_whitelist()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
@bot.tree.command(name="whitelist", description="Whitelists a user and sends them a private invite.")
async def whitelist_command(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You must be an admin to use this command.", ephemeral=True)
        return
    if str(user.id) in whitelist:
        await interaction.response.send_message(f"{user.mention} is already whitelisted!", ephemeral=True)
        return
    try:
        whitelist[str(user.id)] = {"username": user.name}
        save_whitelist(whitelist)
        embed = discord.Embed(
            title="You're Whitelisted!",
            description="You've been given access to our private Discord server. Click the button below to join!",
            color=discord.Color.green()
        )
        embed.add_field(name="Invite Link", value=f"[Join Now]({PRIVATE_SERVER_INVITE})", inline=False)
        await user.send(embed=embed)
        await interaction.response.send_message(f"{user.mention} has been whitelisted and sent an invite!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"⚠️ {user.mention} has DMs disabled! Please ask them to enable DMs.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

bot.run(TOKEN)