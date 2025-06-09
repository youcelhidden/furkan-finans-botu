import requests
import time
import schedule
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = "7878308274:AAG7bxP7gfkbujj0A5L8GGKkCFVaYu_jUEw"
CHAT_ID = "1222943089"

def get_market_data():
    url = "https://www.doviz.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    def get_text(key, attr="s"):
        tag = soup.select_one(f'span[data-socket-key="{key}"][data-socket-attr="{attr}"]')
        if tag:
            value = tag.text.strip().replace("₺", "").replace("$", "").replace(".", "").replace(",", ".")
            try:
                return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return tag.text.strip()
        return "YOK"

    try:
        euro = get_text("EUR")
        dolar = get_text("USD")
        altin = get_text("gram-altin")
        borsa = get_text("XU100")
        bitcoin = get_text("bitcoin", attr="s")
        gumus = get_text("gumus")
        brent = get_text("BRENT", attr="s")
        return euro, dolar, altin, borsa, bitcoin, gumus, brent
    except:
        return ["HATA"] * 7

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def piyasa_bulteni():
    euro, dolar, altin, borsa, bitcoin, gumus, brent = get_market_data()
    now = datetime.now().strftime("%d.%m.%Y")

    if euro == "YOK" or dolar == "YOK" or borsa == "YOK":
        send_telegram_message(f"⚠️ Veri çekilemedi ({now}) – Lütfen bağlantıyı kontrol et.")
        return

    message = f"""📬 Günlük Piyasa Özeti ({now})
💶 Euro: {euro} TL
💵 Dolar: {dolar} TL
🥇 Gram Altın: {altin} TL
📈 BIST 100: {borsa}
🪙 Bitcoin: ${bitcoin}
🥈 Gümüş: {gumus} TL
🛢️ Brent: ${brent}"""
    send_telegram_message(message)

schedule.every().day.at("10:00").do(piyasa_bulteni)
schedule.every().day.at("18:30").do(piyasa_bulteni)


print("📡 Genişletilmiş Piyasa Botu aktif...")

while True:
    schedule.run_pending()
    time.sleep(60)
