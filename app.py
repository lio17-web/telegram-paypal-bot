import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import random
from datetime import datetime
import os

# 🔐 Token Telegram depuis Render (environment variable)
TOKEN = os.getenv("8014776763:AAG_q_XcAKrPXYkgZ1sG4YzWvlo2-htHoCE")

# Chargement des utilisateurs premium depuis un fichier
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

# Vérifie si l'utilisateur est premium
def is_premium(user_id):
    users = load_users()
    user = users.get(str(user_id))
    if user:
        if datetime.strptime(user["expires_at"], "%Y-%m-%d") > datetime.now():
            return True
    return False

# ✨ Liste des mots premium
mots_premium = [
    {"coréen": "친구", "fr": "Ami", "pron": "chingu"},
    {"coréen": "학교", "fr": "École", "pron": "hakgyo"},
    {"coréen": "음식", "fr": "Nourriture", "pron": "eumsik"},
]

# 💬 Liste des mots gratuits
mots_gratuits = [
    {"coréen": "안녕하세요", "fr": "Bonjour", "pron": "annyeonghaseyo"},
    {"coréen": "감사합니다", "fr": "Merci", "pron": "gamsahamnida"},
    {"coréen": "사랑해요", "fr": "Je t’aime", "pron": "saranghaeyo"},
]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nom = update.effective_user.first_name
    await update.message.reply_text(
        f"🇰🇷 Bienvenue {nom} !\n"
        f"Tape /mot pour apprendre un mot coréen.\n"
        f"✨ Pour plus de contenu : /premium"
    )

# /mot
async def mot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_premium(user_id):
        mot = random.choice(mots_premium)
        await update.message.reply_text(
            f"🌟 Mot Premium :\n\n"
            f"📝 Coréen : {mot['coréen']}\n"
            f"📖 Français : {mot['fr']}\n"
            f"🗣️ Prononciation : {mot['pron']}"
        )
    else:
        mot = random.choice(mots_gratuits)
        await update.message.reply_text(
            f"🈶 Mot gratuit :\n\n"
            f"📝 Coréen : {mot['coréen']}\n"
            f"📖 Français : {mot['fr']}\n"
            f"🗣️ Prononciation : {mot['pron']}\n\n"
            f"🔓 Débloque plus de mots avec /premium"
        )

# /premium
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_premium(user_id):
        await update.message.reply_text("✅ Tu es déjà Premium.")
    else:
        paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=ton@email.com&amount=5.00&currency_code=EUR&item_name=Accès+Premium&custom={user_id}&notify_url=https://tonsite.com/paypal-ipn"
        await update.message.reply_text(
            f"🚀 Pour débloquer l’accès Premium :\n{paypal_link}\n\n"
            f"📌 Après paiement, ton accès sera activé automatiquement."
        )

# 🔁 Lancer le bot
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mot", mot))
    app.add_handler(CommandHandler("premium", premium))

    print("✅ Bot Telegram en ligne...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
