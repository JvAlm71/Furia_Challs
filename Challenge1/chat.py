import os
import threading
import time
import webbrowser
import requests
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from googlesearch import search
from google import genai
from google.genai import types
from flask import Flask, request, render_template, jsonify
import threading, time, webbrowser
from google.generativeai.types import GenerationConfig # Importar
from urllib.request import urlopen, Request
from web_scraping import get_furia_players, fetch_news_summary

# Busca de noticias e jogadores da FURIA
news = fetch_news_summary("furia cs2")
player_names = get_furia_players()

# Configuração do Flask
# Cria a pasta web se não existir
app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",        # <- garante que /styles.css e /chat.js funcionem
    template_folder="web"
)

#Configuração do chat Gemini
client = genai.Client(api_key="AIzaSyAOM2B1asxKdp1SFgid5ALvaCUTA2pqmH4")
history = [ types.UserContent(parts=[types.Part(text="Qual foi o último jogo?")]) ]
config = types.GenerateContentConfig(
    system_instruction=(
        "Você é o assistente oficial de fãs da FURIA Esports (CS2). "
        "Use uma linguagem fácil e acessivel, foque em notícias, escalações e estatísticas."
        "Se não souber a resposta, diga que não tem certeza e sugira verificar o site oficial da FURIA."
        "Evite falar sobre outros jogos ou temas que não sejam CS2."
        "Se o usuário perguntar sobre outros jogos, diga que você é especializado em CS2 e não pode ajudar com isso."
        "Se mantenha atualizado sobre as últimas notícias e eventos da FURIA."
        "Para as perguntas relacionadas a jogo, resultado, placar, noticia, evento,além de mostrar a noticia, de uma breve comentada."
        "Mostre entusiasmo pelas conquistas da FURIA!"
        "Lembre que voce é um assistente de fãs, não um bot de suporte técnico ou vendas."
    ),
    temperature=0.5,
)

chat = client.chats.create(model="gemini-2.0-flash", config=config, history=history)


# --- Rotas Flask ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    key = msg.strip().lower()

    if any(k in key for k in ("escalacao","escalação","formacao","formação","lineup","roster","line-up")):
        escala = ", ".join(player_names)
        # Peça ao Gemini um comentário sobre o time, usando o input do usuário
        prompt = (
            f"Usuário pediu a escalação e um comentário: '{msg}'. "
            f"A escalação é: {escala}. "
            "Faça um comentário breve e empolgado sobre o time e a escalação."
        )
        resp = chat.send_message(prompt)
        reply = f"A formação atual da FURIA é: {escala}<br><br>{resp.text}"
    elif any(k in key for k in ("noticia","noticias","notícia","notícias")):
        reply = fetch_news_summary(msg)
    else:
        resp = chat.send_message(msg)
        reply = resp.text

    return jsonify({"reply": reply})


def open_browser():
    # aguarda o Flask subir
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

# Inicia thread para abrir o browser
#threading.Thread(target=open_browser, daemon=True).start()


# endpoint de shutdown (aceita GET e POST)
@app.route("/shutdown", methods=["GET", "POST"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    else:
        # fallback: mata o processo imediatamente
        os._exit(0)
    return "Server shutting down...", 200


# --- Helper para abrir o browser APENAS UMA VEZ ---
def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    # Desliga o reloader para abrir só UMA aba
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)
