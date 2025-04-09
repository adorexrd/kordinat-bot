import discord
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
import os
import math

# CONFIG
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
MONGO_URI = "YOUR_MONGODB_CONNECTION_STRING"
GEREKLI_ROL_ID = 1359281485189873724  # Değiştirin

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
client = MongoClient(MONGO_URI)
db = client["titanyum"]
hesaplar = db["hesaplar"]

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="Adorexrd ❤"))
    print(f"Bot giriş yaptı: {bot.user}")

def rol_kontrol(interaction):
    return GEREKLI_ROL_ID in [r.id for r in interaction.user.roles]

@bot.tree.command(name="hesapekle", description="Yeni hesap ekle")
@app_commands.describe(
    isim="Hesabın adı",
    sancak="Sancak X Z",
    yakamoz="Yakamoz X Z",
    avrasya="Avrasya X Z",
    pruva="Pruva X Z",
    velena="Velena X Z",
    flador="Flador X Z",
    astra="Astra X Z"
)
async def hesapekle(
    interaction: discord.Interaction,
    isim: str,
    sancak: str,
    yakamoz: str,
    avrasya: str,
    pruva: str,
    velena: str,
    flador: str,
    astra: str
):
    if not rol_kontrol(interaction):
        return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

    if hesaplar.find_one({"isim": isim}):
        return await interaction.response.send_message("❌ Bu hesap zaten var.", ephemeral=True)

    def parse_coords(girdi):
        try:
            x_str, z_str = girdi.strip().split()
            x = int(x_str)
            z = int(z_str)
            if not (-30000 <= x <= 30000 and -30000 <= z <= 30000):
                return "out_of_bounds"
            return {"x": x, "z": z}
        except:
            return None

    veri = {
        "isim": isim,
        "dunyalar": {
            "sancak": parse_coords(sancak),
            "yakamoz": parse_coords(yakamoz),
            "avrasya": parse_coords(avrasya),
            "pruva": parse_coords(pruva),
            "velena": parse_coords(velena),
            "flador": parse_coords(flador),
            "astra": parse_coords(astra),
        }
    }

    if any(v is None for v in veri["dunyalar"].values()):
        return await interaction.response.send_message("❌ Koordinat formatı hatalı. Örn: `30 -2`", ephemeral=True)

    if any(v == "out_of_bounds" for v in veri["dunyalar"].values()):
        return await interaction.response.send_message("❌ -30k ve 30k koordinatlar girebilirsiniz.", ephemeral=True)

    hesaplar.insert_one(veri)

    embed = discord.Embed(title="✅ Hesap Eklendi", description=f"`{isim}` başarıyla eklendi.", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hesapsil", description="Bir hesabı sil")
@app_commands.describe(isim="Silinecek hesap adı")
async def hesapsil(interaction: discord.Interaction, isim: str):
    if not rol_kontrol(interaction):
        return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

    sonuc = hesaplar.delete_one({"isim": isim})
    if sonuc.deleted_count == 0:
        return await interaction.response.send_message("❌ Böyle bir hesap bulunamadı.", ephemeral=True)

    embed = discord.Embed(title="🗑️ Hesap Silindi", description=f"`{isim}` adlı hesap silindi.", color=0xff0000)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kordinat", description="Koordinatlara göre en yakın hesabı bul")
@app_commands.describe(dunya="Dünya adı", kordinat="X Z şeklinde koordinat")
async def kordinat(interaction: discord.Interaction, dunya: str, kordinat: str):
    try:
        x_str, z_str = kordinat.strip().split()
        x, z = int(x_str), int(z_str)
    except ValueError:
        return await interaction.response.send_message("❌ Koordinat formatı yanlış. Örn: -30 20", ephemeral=True)

    dunya = dunya.lower()
    en_yakin_hesap = None
    min_mesafe = float("inf")
    en_yakin_koordinat = (0, 0)

    for hesap in hesaplar.find():
        koordinatlar = hesap["dunyalar"].get(dunya)
        if not koordinatlar:
            continue

        hx = koordinatlar["x"]
        hz = koordinatlar["z"]
        mesafe = math.sqrt((hx - x) ** 2 + (hz - z) ** 2)

        if mesafe < min_mesafe:
            min_mesafe = mesafe
            en_yakin_hesap = hesap
            en_yakin_koordinat = (hx, hz)

    if en_yakin_hesap:
        embed = discord.Embed(
            title="📍 En Yakın Hesap",
            color=0x2ecc71
        )
        embed.add_field(name="Dünya", value=dunya.capitalize(), inline=False)
        embed.add_field(name="En Yakın Hesap", value=en_yakin_hesap['isim'], inline=False)
        embed.add_field(name="En Yakın Hesap Koordinatı", value=f"{en_yakin_koordinat[0]} {en_yakin_koordinat[1]}", inline=False)
        embed.add_field(name="Aradığınız Koordinat", value=f"{x} {z}", inline=False)
        embed.add_field(name="Mesafe", value=f"{int(round(min_mesafe))} blok", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ Uygun hesap bulunamadı.", ephemeral=True)

bot.run(TOKEN)
