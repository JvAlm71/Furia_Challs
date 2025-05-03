import os
import threading
import time
import webbrowser
import requests
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from flask import Flask, request, render_template, jsonify
import google.generativeai.types 
from urllib.request import urlopen, Request
from web_scraping import get_furia_players, fetch_news_summary
from dotenv import load_dotenv



load_dotenv() 

news = fetch_news_summary("furia cs2")
player_names = get_furia_players()

# Configuração do Flask
app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",
    template_folder="web"
)

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Verifica se a chave foi carregada
if not gemini_api_key:
    print("Erro: Chave da API Gemini não encontrada.")
    print("Certifique-se de criar um arquivo .env com GEMINI_API_KEY='sua_chave'")
    exit() # Encerra o script se a chave não estiver presente

client = genai.Client(api_key=gemini_api_key)
history = [ types.UserContent(parts=[types.Part(text="Qual foi o último jogo?")])]

config = types.GenerateContentConfig(
    temperature=0.5,
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
 
)

chat = client.chats.create(model="gemini-2.0-flash", config=config, history=history,) 

# --- Rotas Flask ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    key = msg.strip().lower()
    reply = "" 

    try: 
        if any(k in key for k in ("escalacao","escalação","formacao","formação","lineup","roster","line-up")):
            escala = ", ".join(player_names)
            prompt = (
                f"Usuário pediu a escalação e um comentário: '{msg}'. "
                f"A escalação atual da FURIA (obtida do HLTV) é: {escala}. "
                "Faça um comentário breve e empolgado sobre o time e a escalação atual."
            )
            resp = chat.send_message(prompt)
            reply = f"A formação atual da FURIA é: {escala}<br><br>{resp.text}"
        elif any(k in key for k in ("noticia","noticias","notícia","notícias")):
            # A função fetch_news_summary já trata o caso de não encontrar notícias
            reply = fetch_news_summary(key) # Passa a chave para buscar notícias relacionadas
        else:
            resp = chat.send_message(msg)
            reply = resp.text

    except Exception as e:
        print(f"Erro durante o processamento do chat: {e}")
        reply = "Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente."

    return jsonify({"reply": reply})


# --- Helper para abrir o browser APENAS UMA VEZ ---
browser_opened = False
def open_browser():
    global browser_opened
    if not browser_opened:
        # aguarda o Flask subir
        time.sleep(1)
        print("--- Abrindo navegador em http://localhost:8000 ---")
        webbrowser.open("http://localhost:8000")
        browser_opened = True


# endpoint de shutdown (aceita GET e POST)
@app.route("/shutdown", methods=["GET", "POST"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        print("--- Desligando servidor via Werkzeug ---")
        func()
    else:
        # fallback: mata o processo imediatamente
        print("--- Desligando servidor via os._exit ---")
        os._exit(0)
    return "Servidor desligando...", 200


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("--- Iniciando servidor Flask ---")
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)