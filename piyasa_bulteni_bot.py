import requests
import time
import schedule
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = "7878308274:AAG7bxP7gfkbujj0A5L8GGKkCFVaYu_jUEw"
CHAT_ID = "1222943089"

def get_market_data():
    try:
        url = "https://www.doviz.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        euro = soup.find("span", {"data-socket-key": "EUR"})
        dolar = soup.find("span", {"data-socket-key": "USD"})
        altin = soup.find("span", {"data-socket-key": "GA"})
        borsa = soup.find("span", {"data-socket-key": "XU100"})

        euro = float(euro.text.strip().replace(",", ".")) if euro else None
        dolar = float(dolar.text.strip().replace(",", ".")) if dolar else None
        altin = float(altin.text.strip().replace(",", ".")) if altin else None
        borsa = borsa.text.strip() if borsa else "Veri Yok"

        return euro, dolar, altin, borsa
    except Exception as e:
        return None, None, None, None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def sabah_bulteni():
    euro, dolar, altin, borsa = get_market_data()
    now = datetime.now().strftime("%d.%m.%Y")

    if euro and dolar:
        message = f"""📬 Sabah Bülteni ({now})
💶 Euro: {euro} TL
💵 Dolar: {dolar} TL"""
        if altin: message += f"\n🥇 Altın: {altin} TL"
        if borsa: message += f"\n📈 BIST: {borsa}"
    else:
        message = f"⚠️ Euro veya Dolar verisi çekilemedi ({now})"

    send_telegram_message(message)


# schedule.every().day.at("10:00").do(sabah_bulteni)
# schedule.every().day.at("18:30").do(aksam_bulteni)
schedule.every(1).minutes.do(sabah_bulteni)

print("📡 Furkan Finansal Bülten Botu aktif...")

while True:
    schedule.run_pending()
    time.sleep(60)
