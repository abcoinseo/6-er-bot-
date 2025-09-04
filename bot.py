import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----- Inline Firebase Service Account -----
service_account_info = {
  "type": "service_account",
  "project_id": "clint-bot-101",
  "private_key_id": "190b5be12bf62c8cfea2ce0f1492f1b0b923898b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD2tCdXY/EcHewb\nBJhmBpNUptV5q46LA31Ie8M/GHbHnc/H8ELQXvN5E+J3XCizzra6IvjavbGmh689\nmpmmwh4gFU7R2Rc2FgCKBjtXpZNCOFeOzi3NLYS08k5Q+1C81nyfi9PUUfYGmQYq\nKvIgSE3g60kapjtzDf6IpN6V7+2nK0g6CbWsNdcFoMjZrD1EpmwHePH8mptuoC5g\nbd93R7RIeI9hUS3ecWgyQUdKjm/dbfE4aawrVuCW6gVJQwikWVCJKZBhAn4WXSEz\nOIC0q1oxbBpNsDSn0azmKiJWYrgFx3lMUuVojBAo98CsBmyYBp1sNa2jojqAT1mu\nx6V53nlTAgMBAAECggEAAtw3HaRxt1x2ik69sfKTYxI56qZLz4Emq5p2o2ZEqkZZ\nkiusNNDK0jVziW/Ruys3o3zSfia9O0MJRf56gHlaOGyj6MEcH/bEnKaBHlp5oDsZ\nijrbiRVCMvvyvCJZao5Vr41O6oAq8d1daGMFQodIb90hvu9ZuLvycBCU6ScEmczQ\nShc71w0u/sU8ttWxYTCobOkHd0Giv8A/dqLVTYif2J7zXVCOUezQuLZB8rA7Kt49\nY0SXGJz7m9j1FvQRoVjamTzU0290uLKlKi/V5Gccvx2d2xXjuxCszLKTY5K6hBya\nCzTTMEJlwC3zQd8tRuws66wj3zNn2tktJVmOwqOpQQKBgQD/seq+1O18ggu4dCtw\nmR13nt+zdvnCwXe4MiLdl0QL44gXgzmCdKWNOYPI/wpWIIrq+A/lCKD9g3zfz4m4\nO8nYntocFXEq60VRCl+emuPRXXjpsld02h8Z2ToFOR4FmMwqno0zH+aGyRsNCk93\nYGjxzAQb6ixR/xQlFIQu4ulr4wKBgQD2/32xhcUfK3mr2Mb9r5C92Z7v5GRSLNpQ\nsvDLOzETXHZSxyWyyTjsSIliiEkYgoXykcVZE7ycp6pVl/Z/puGSxulA3txvuW0x\nV37eGZBCbRjIG6WZUVQJXmCd5CK6x7JbbIuc2HAN7XhtXeCn0GVN1CayOtZXW9KE\nLyFOF7QX0QKBgQCen/CCfLPsBv1ga+k7DDIksJIU0t11PfKYebn5gEr9mSUneQgn\nb1f4+dJQ0i/GaJ/lzwiFTMobHARPEIBeo/C/iyTCQWcYeiZhdS8GxQ5KJ1PInxP0\ncRDUR1fgP6PpUvZuBjiQm9y2h3JZr6jG5S+Vubxe2PKv16/WpRivwaOPgwKBgBFa\nCX57I0n5R+bmp7QSrVxo+V1o8hNDy2J376qXUe9GQ5m1G9TfhfwzbFNbt6bdJIPR\n8cc8N7fZn4G71zlIg/hHuQMxpNLEeANLXkJEEXpZJ7CHIK8Qo5K06pys9jOg68q4\naWZvXg/cauVj/vBLF5LMIJvMvloMvVFD7lcKG0DBAoGBANvPfDIJnIDu3/rxRMTs\nd2CwK/oiFAEYHgrdkm/l/2QnDAjWvzQemajU+ZDsEsMt53RgyUNrZaX3Hngfzl7V\nQVw6GYIXJVuO0jyrni1ncvrzidbFmNf49fM+g90bSbtCQopqO+h7aJxfF2jQOGrM\n1CGxJ8BOQBA6Uf+Ehzx7iLef\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@clint-bot-101.iam.gserviceaccount.com",
  "client_id": "101125116889276579512",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40clint-bot-101.iam.gserviceaccount.com"
}

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://clint-bot-101-default-rtdb.firebaseio.com/'
})

logging.info("Firebase initialized successfully ✅")

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # <-- change this

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ref = db.reference(f'users/{update.effective_user.id}')
    data = user_ref.get()
    if not data:
        user_ref.set({
            "username": update.effective_user.username,
            "first_name": update.effective_user.first_name
        })
    await update.message.reply_text("Bot is running! 🚀")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

logging.info("Bot is running 🚀")
app.run_polling()
