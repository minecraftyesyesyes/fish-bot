import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
from datetime import datetime

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

tree = bot.tree

FISH_TYPES = [
    "Goldfish",
    "Shark",
    "Salmon",
    "Tuna",
    "Pufferfish",
    "Catfish",
    "Swordfish",
    "Clownfish",
    "Eel",
    "Whale Shark",
    "Blobfish",
]

FISH_FACTS = [
    "Some fish can recognize human faces.",
    "Sharks existed before trees.",
    "Pufferfish puff up to scare predators.",
    "Goldfish can learn tricks.",
    "Some fish sleep with eyes open.",
    "Catfish have taste buds all over their bodies.",
]

LEGENDARY_FISH = [
    "Golden Megalodon",
    "Ultra Trout",
    "Cosmic Pufferfish",
    "Ancient Blobfish",
]

DATA_FILE = "leaderboard.json"

def load_scores():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_scores(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_score(user_id):
    data = load_scores()
    uid = str(user_id)
    data[uid] = data.get(uid, 0) + 1
    save_scores(data)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")

@tree.command(name="fish", description="Shows a fish image")
async def fish(interaction: discord.Interaction):
    url = "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781558584419/the-rainbow-fish-big-book-pb-9781558584419_hr.jpg"

    embed = discord.Embed(title="fish")
    embed.set_image(url=url)

    await interaction.response.send_message(embed=embed)

@tree.command(name="sayfish", description="Says fish")
async def sayfish(interaction: discord.Interaction):
    await interaction.response.send_message("fish")
    
@tree.command(name="cp", description="child....")
async def cp(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.cplegacy.com/")

@tree.command(name="fishsomeone", description="Fishes someone")
@app_commands.describe(user="Person to fish")
async def fishsomeone(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(
        f"{interaction.user.mention} has fished {user.mention}!!! what a silly fish"
    )

@tree.command(name="fishin", description="Random fish")
async def fishin(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(FISH_TYPES))

@tree.command(name="fishcredits", description="Credits")
async def fishcredits(interaction: discord.Interaction):
    await interaction.response.send_message("made by monkez3623 and silliest_dude_ever on discord")
    
@tree.command(name="pufferfish", description="Piffer")
async def pufferfish(interaction: discord.Interaction):
    file = discord.File("augh.mp3")
    await interaction.response.send_message(file=file)

@tree.command(name="fishhelp", description="Help")
async def fishhelp(interaction: discord.Interaction):
    await interaction.response.send_message("no help im lazy :)")

@tree.command(name="dailyfish", description="Random fish every day")
async def dailyfish(interaction: discord.Interaction):
    today = datetime.now().strftime("%Y-%m-%d")
    random.seed(today)
    fish_name = random.choice(FISH_TYPES)
    await interaction.response.send_message(f"Today's fish is: {fish_name}")

@tree.command(name="ratefish", description="Rate a fish")
async def ratefish(interaction: discord.Interaction):
    fish_name = random.choice(FISH_TYPES)
    rating = random.randint(1, 10)
    await interaction.response.send_message(f"{fish_name}: {rating}/10")

@tree.command(name="battlefish", description="Battle another user")
@app_commands.describe(user="User to battle")
async def battlefish(interaction: discord.Interaction, user: discord.Member):
    winner = random.choice([interaction.user, user])
    await interaction.response.send_message(
        f"Fish battle between {interaction.user.mention} and {user.mention}!\nWinner: {winner.mention}"
    )

@tree.command(name="rarefish", description="1% chance legendary fish")
async def rarefish(interaction: discord.Interaction):
    chance = random.randint(1, 100)
    if chance == 1:
        fish_name = random.choice(LEGENDARY_FISH)
        await interaction.response.send_message(f"notrarefishis{fish_name}")
    else:
        await interaction.response.send_message("rarefish")

@tree.command(name="fishfact", description="Random fish fact")
async def fishfact(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(FISH_FACTS))

@tree.command(name="fishleaderboard", description="Leaderboard")
async def fishleaderboard(interaction: discord.Interaction):
    data = load_scores()

    if not data:
        await interaction.response.send_message("No fishers yet.")
        return

    sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)

    msg = "🏆 Fish Leaderboard:\n"
    for i, (uid, score) in enumerate(sorted_users[:10], start=1):
        msg += f"{i}. <@{uid}> - {score}\n"

    await interaction.response.send_message(msg)

@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.application_command:
        add_score(interaction.user.id)
    await bot.process_application_commands(interaction)

bot.run(TOKEN)
