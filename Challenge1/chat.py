import requests
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from googlesearch import search
from google import genai
from google.genai import types

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

# Busca de notícias via Google News RSS
def fetch_news_summary(query: str) -> str:
    q = urllib.parse.quote(f"{query} FURIA CS2")
    rss_url = f"https://news.google.com/rss/search?q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return "Não encontrei notícias recentes. Confira https://furia.gg"
    itens = feed.entries[:3]
    return "\n\n".join(f"• {e.title}\n  {e.link}" for e in itens)

#Saudação
welcome = "Olá! Eu sou o chatbot oficial da FURIA CS2. Pergunte o que quiser!"
print("Chatbot:", welcome)
chat.send_message(welcome)

#Loop de interação
while True:
    user_input = input("Você: ").strip().lower()
    if user_input in ("sair", "exit", "quit"):
        print("Chatbot: Até a próxima! 💥")
        break

    # notícias / resultado
    if any(k in user_input for k in ("jogo", "resultado", "placar", "noticia", "evento")):
        print("Chatbot: Aqui vão as notícias mais recentes:")
        print(fetch_news_summary(user_input))
        continue

    # fallback para Gemini
    resp = chat.send_message(user_input)
    print("Chatbot:", resp.text)
