import discord
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
import os
import math

# CONFIG
TOKEN = "token gir"
MONGO_URI = "mongo url"
GEREKLI_ROL_ID = 1411131197131591821  # Değiştirin

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

@bot.tree.command(name="kordinat", description="Koordinatlara göre en yakın hesapları bul")
@app_commands.describe(dunya="Dünya adı", kordinat="X Z şeklinde koordinat")
async def kordinat(interaction: discord.Interaction, dunya: str, kordinat: str):
    try:
        x_str, z_str = kordinat.strip().split()
        x, z = int(x_str), int(z_str)
    except ValueError:
        return await interaction.response.send_message("❌ Koordinat formatı yanlış. Örn: -30 20", ephemeral=True)

    dunya = dunya.lower()
    hesap_mesafeleri = []

    for hesap in hesaplar.find():
        koordinatlar = hesap["dunyalar"].get(dunya)
        if not koordinatlar:
            continue

        hx, hz = koordinatlar["x"], koordinatlar["z"]
        mesafe = math.sqrt((hx - x) ** 2 + (hz - z) ** 2)
        hesap_mesafeleri.append((mesafe, hesap["isim"], (hx, hz)))

    if not hesap_mesafeleri:
        return await interaction.response.send_message("❌ Uygun hesap bulunamadı.", ephemeral=True)

    hesap_mesafeleri.sort(key=lambda t: t[0])

    # Embed oluştur
    embed = discord.Embed(
        title=f"📍 En Yakın Hesaplar ({dunya.capitalize()})",
        color=0x1abc9c
    )
    embed.add_field(name="Aradığınız Koordinat", value=f"`{x} {z}`", inline=False)

    # En yakın 3 hesabı ekle
    for i, (mesafe, isim, (hx, hz)) in enumerate(hesap_mesafeleri[:3], start=1):
        embed.add_field(
            name=f"{i}. En Yakın Hesap",
            value=f"**{isim}**\nKoordinat: `{hx} {hz}`\nMesafe: `{int(round(mesafe))} blok`",
            inline=False
        )

    # Footer ekle: Kullanıcı ve saat
    embed.set_footer(
        text=f"Kullanıcı: {interaction.user} | Tarih: {interaction.created_at.strftime('%d-%m-%Y %H:%M:%S')}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else None
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hesaplar", description="Sistemdeki toplam hesap sayısını gösterir")
async def hesaplar_command(interaction: discord.Interaction):
    toplam_hesap = hesaplar.count_documents({})  # Veritabanındaki tüm hesapları say

    embed = discord.Embed(
        title="📊 Toplam Hesaplar",
        description=f"Sistemde toplam **{toplam_hesap}** hesap bulunmaktadır.",
        color=0x3498db
    )

    # Footer: Komutu kullanan kişi ve tarih
    embed.set_footer(
        text=f"Kullanıcı: {interaction.user} | Tarih: {interaction.created_at.strftime('%d-%m-%Y %H:%M:%S')}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else None
    )

    await interaction.response.send_message(embed=embed)



bot.run(TOKEN)
