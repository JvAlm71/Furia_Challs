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


app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",        # <- garante que /styles.css e /chat.js funcionem
    template_folder="web"
)


#Configuração do chat Gemini
client = genai.Client(api_key="AIzaSyAOM2B1asxKdp1SFgid5ALvaCUTA2pqmH4")
config = types.GenerateContentConfig(
    system_instruction=(
        "Você é o assistente oficial de fãs da FURIA Esports (CS2). "
        "Use tom jovem, irreverente e foque em notícias, escalações e estatísticas."
        "Sempre comece o chat lembrando que é um assistente de fãs e não um bot de suporte."
        "Se não souber a resposta, diga que não tem certeza e sugira verificar o site oficial da FURIA."
        "Tente ser divertido e engajante, mas não ultrapasse os limites do respeito."
        "Evite falar sobre outros jogos ou temas que não sejam CS2."
        "Se o usuário perguntar sobre outros jogos, diga que você é especializado em CS2 e não pode ajudar com isso."
        "Se mantenha atualizado sobre as últimas notícias e eventos da FURIA."
        "Para as perguntas relacionadas a jogo, resultado, placar, noticia, evento,além de mostrar a noticia, de uma breve comentada."
    )
)
history = [ types.UserContent(parts=[types.Part(text="Qual foi o último jogo?")]) ]
chat = client.chats.create(model="gemini-2.0-flash", config=config, history=history)

# Busca de notícias via Google News RSS (retorna HTML com links clicáveis)
def fetch_news_summary(query: str) -> str:
    q = urllib.parse.quote(f"{query} FURIA CS2")
    rss_url = f"https://news.google.com/rss/search?q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return (
            'Não encontrei notícias recentes. '
            '<a href="https://furia.gg" target="_blank" rel="noopener">Visite o site oficial da FURIA</a>'
        )
    html = ""
    for entry in feed.entries[:3]:
        title = entry.title
        link  = entry.link
        html += (
            f'<div class="news-item">• '
            f'<a href="{link}" target="_blank" rel="noopener">{title}</a>'
            f'</div>'
        )
    return html


#Saudação
welcome = "Olá! Eu sou o chatbot oficial da FURIA CS2. Pergunte o que quiser!"
print("Chatbot:", welcome)
chat.send_message(welcome)


# --- Rotas Flask ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    key = msg.strip().lower()

    # notícias / resultado
    if any(k in key for k in ("noticia","noticias","notícia","notícias")):
        reply = fetch_news_summary(msg)
    else:
        resp = chat.send_message(msg)
        reply = resp.text

    return jsonify({ "reply": reply })


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
