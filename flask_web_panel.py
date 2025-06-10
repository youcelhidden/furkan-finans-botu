from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("data/market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"euro": "YOK", "dolar": "YOK", "altin": "YOK", "borsa": "YOK", "bitcoin": "YOK", "gumus": "YOK", "brent": "YOK", "tarih": "Veri yok"}

    html = """
    <html>
    <head>
        <title>Furkan Finans Paneli</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; text-align: center; background: #f9f9f9; padding: 20px; }
            .card { background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); margin: 10px auto; padding: 20px; max-width: 400px; }
            h1 { color: #444; }
            .veri { font-size: 1.2em; margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>📈 Günlük Piyasa Verileri</h1>
        <div class="card">
            <div class="veri">💶 Euro: {{ data.euro }} TL</div>
            <div class="veri">💵 Dolar: {{ data.dolar }} TL</div>
            <div class="veri">🥇 Altın: {{ data.altin }} TL</div>
            <div class="veri">📈 BIST100: {{ data.borsa }}</div>
            <div class="veri">🪙 Bitcoin: ${{ data.bitcoin }}</div>
            <div class="veri">🥈 Gümüş: {{ data.gumus }} TL</div>
            <div class="veri">🛢️ Brent: ${{ data.brent }}</div>
            <div class="veri">📅 Tarih: {{ data.tarih }}</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

if __name__ == "__main__":
    app.run(debug=True)
