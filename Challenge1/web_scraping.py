from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.parse
import feedparser
import requests
import json
import os
import time
import threading

def get_furia_players():
    url = "https://www.hltv.org/team/8297/furia"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    req = Request(url, headers=headers)
    html = urlopen(req)
    bs = BeautifulSoup(html, "html.parser")
    player_spans = bs.find_all("span", class_="text-ellipsis bold")
    player_names = [span.get_text(strip=True) for span in player_spans]
    return player_names

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