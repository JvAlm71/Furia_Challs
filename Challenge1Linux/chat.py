import os
import threading
import time
import webbrowser
import requests
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
import google.generativeai as genai       
from flask import Flask, request, render_template, jsonify
from urllib.request import urlopen, Request
from web_scraping import get_furia_players, fetch_news_summary
from dotenv import load_dotenv

load_dotenv()

# coleta de news/jogadores
news = fetch_news_summary("furia cs2")
player_names = get_furia_players()

app = Flask(__name__, static_folder="web", static_url_path="", template_folder="web")

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("Erro: Chave da API Gemini não encontrada.")
    exit()

# configura SDK
genai.configure(api_key=gemini_api_key)

# system prompt
SYSTEM = (
    "Você é o assistente oficial de fãs da FURIA Esports (CS2). "
    "Use linguagem fácil e acessível, foque em notícias, escalações e estatísticas. "
    "Se não souber, diga que não tem certeza e sugira o site oficial da FURIA. "
    "Evite outros jogos; se perguntarem, avise que só sabe de CS2. "
    "Mantenha-se atualizado sobre notícias e eventos da FURIA. "
    "Para perguntas de resultado, placar, notícia, faça um breve comentário. "
    "Mostre entusiasmo pelas conquistas da FURIA! "
    "Você é um assistente de fãs, não um bot de suporte técnico ou vendas."
)

# helper de chamada única
def ask_gemini(user_msg: str) -> str:
    mensagens = [
        {"author": "system", "content": SYSTEM},
        {"author": "user",   "content": user_msg}
    ]
    resp = genai.chat.completions.create(
        model="gemini-2.0-flash",
        messages=mensagens,
        temperature=0.5,
    )
    return resp.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    msg = data.get("message", "").strip()
    key = msg.lower()

    if any(k in key for k in ("escalacao","escalação","formacao","formação","lineup","roster","line-up")):
        escala = ", ".join(player_names)
        prompt = f"Usuário pediu a escalação e um comentário: '{msg}'. A escalação é: {escala}."
        gemini_reply = ask_gemini(prompt)
        reply = f"A formação atual da FURIA é: {escala}<br><br>{gemini_reply}"
    elif any(k in key for k in ("noticia","noticias","notícia","notícias")):
        reply = fetch_news_summary(msg)
    else:
        reply = ask_gemini(msg)

    return jsonify({"reply": reply})

def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

@app.route("/shutdown", methods=["GET","POST"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func: func()
    else: os._exit(0)
    return "Server shutting down...", 200

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)