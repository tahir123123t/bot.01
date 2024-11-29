import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

message_history = {}
user_points = {}
admin_id = 788423955827392573  # Kurucunun Discord ID'si (kendi ID'niz ile değiştirin)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        await bot.tree.sync()  # Slash komutlarını senkronize et
        print('Slash komutları senkronize edildi.')
    except Exception as e:
        print(f'Senkronize edilemedi: {e}')

@bot.tree.command(name="test", description="Test komutu")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('Test mesajı!')

@bot.tree.command(name="zar", description="Zar atar")
async def zar(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in user_points:
        user_points[user_id] = 0
    
    current_points = user_points[user_id]
    probability = max(1, 100 - current_points // 1000)  # Puanlara bağlı olarak şans azalır (örnek formül)
    roll = random.randint(1, 100)
    
    if roll <= probability:
        point = random.randint(1, 10000000000)
    else:
        point = 0

    user_points[user_id] += point
    await interaction.response.send_message(f'Sonuç: {point}. Toplam puanınız: {user_points[user_id]} (Şans: %{probability})')

@bot.tree.command(name="selam", description="Selam verir")
async def selam(interaction: discord.Interaction):
    await interaction.response.send_message('Merhaba! Ben buradayım.')

@bot.tree.command(name="puan", description="Toplam puanınızı gösterir")
async def puan(interaction: discord.Interaction):
    user_id = interaction.user.id
    points = user_points.get(user_id, 0)
    await interaction.response.send_message(f'Toplam zar puanınız: {points}')

@bot.tree.command(name="magaza", description="Mağazayı gösterir")
async def magaza(interaction: discord.Interaction):
    shop_items = (
        "**Şanslı Amulet**: 10,000,000 puan (Şansını %10 artırır)\n"
        "**Kutsal Tılsım**: 20,000,000 puan (Şansını %15 artırır)\n"
        "**Efsanevi Yüzük**: 50,000,000 puan (Şansını %20 artırır)\n"
        "**Gizemli Kolye**: 100,000,000 puan (Şansını %25 artırır)\n"
        "**Kadim Kitap**: 200,000,000 puan (Şansını %30 artırır)\n"
        "**Gökkuşağı Taşı**: 500,000,000 puan (Şansını %35 artırır)\n"
        "**Kutsal Asa**: 1,000,000,000 puan (Şansını %40 artırır)\n"
        "**Efsanevi Miğfer**: 2,000,000,000 puan (Şansını %45 artırır)\n"
        "**Sihirli Pelerin**: 5,000,000,000 puan (Şansını %50 artırır)\n"
        "**Evrenin Anahtarı**: 10,000,000,000 puan (Şansını %60 artırır)\n"
    )
    await interaction.response.send_message(f'**Mağazamıza hoş geldiniz!**\n{shop_items}\nBir eşya satın almak için `/satin_al <eşya_adı>` komutunu kullanın.')

@bot.tree.command(name="satin_al", description="Mağazadan eşya satın alır")
async def satin_al(interaction: discord.Interaction, item_name: str):
    user_id = interaction.user.id
    points = user_points.get(user_id, 0)
    items = {
        "şanslı amulet": {"fiyat": 10000000, "etki": "Şansını %10 artırır"},
        "kutsal tılsım": {"fiyat": 20000000, "etki": "Şansını %15 artırır"},
        "efsanevi yüzük": {"fiyat": 50000000, "etki": "Şansını %20 artırır"},
        "gizemli kolye": {"fiyat": 100000000, "etki": "Şansını %25 artırır"},
        "kadim kitap": {"fiyat": 200000000, "etki": "Şansını %30 artırır"},
        "gökkuşağı taşı": {"fiyat": 500000000, "etki": "Şansını %35 artırır"},
        "kutsal asa": {"fiyat": 1000000000, "etki": "Şansını %40 artırır"},
        "efsanevi miğfer": {"fiyat": 2000000000, "etki": "Şansını %45 artırır"},
        "sihirli pelerin": {"fiyat": 5000000000, "etki": "Şansını %50 artırır"},
        "evrenin anahtarı": {"fiyat": 10000000000, "etki": "Şansını %60 artırır"}
    }
    
    item = items.get(item_name.lower())
    if item and points >= item['fiyat']:
        user_points[user_id] -= item['fiyat']
        await interaction.response.send_message(f'{item_name} satın aldınız! {item["etki"]}. Kalan puanınız: {user_points[user_id]}')
    else:
        await interaction.response.send_message(f'Eşya bulunamadı veya yeterli puanınız yok.')

@bot.tree.command(name="setpoint", description="Kullanıcı puanını ayarlar")
@app_commands.checks.has_permissions(administrator=True)  # Sadece kurucu kullanabilir
async def setpoint(interaction: discord.Interaction, user: discord.User, points: int):
    if interaction.user.id == admin_id:
        user_points[user.id] = points
        await interaction.response.send_message(f'Kullanıcı {user.name} için puan {points} olarak ayarlandı.')
    else:
        await interaction.response.send_message('Bu komutu kullanma yetkiniz yok.')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='genel')
    if channel:
        await channel.send(f'Hoş geldin, {member.mention}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    log_channel = discord.utils.get(message.guild.channels, name='loglar')
    if log_channel:
        await log_channel.send(f'{message.author}: {message.content}')

    if check_spam(message):
        await message.author.ban(reason="Spam yapmak", delete_message_days=1)

    await bot.process_commands(message)

def check_spam(message):
    now = datetime.now()
    author_id = message.author.id
    if author_id not in message_history:
        message_history[author_id] = []
    message_history[author_id].append(now)

    # Mesaj geçmişini temizle, sadece son 10 saniyeyi tut
    message_history[author_id] = [msg_time for msg_time in message_history[author_id] if now - msg_time < timedelta(seconds=10)]

    # Son 10 saniyede 5'ten fazla mesaj varsa spam olarak kabul et
    if len(message_history[author_id]) > 5:
        return True
    return False

bot.run('UR TOKEN HERE')
