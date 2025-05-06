# Relatório e Documentação do Projeto: Chatbot FURIA FANS

**Autor:** João Victor de Almeida
**Projeto:** Chatbot Interativo para Fãs da FURIA Esports (CS2) - Processo Seletivo de Assistente de Engenharia de Software

## 1. Introdução e Visão Geral

Este projeto consiste em um chatbot web interativo desenvolvido como parte do processo seletivo. O objetivo principal é criar uma interface de conversação para fãs da equipe de Counter-Strike 2 (CS2) da FURIA Esports, fornecendo informações relevantes como escalação atual, notícias recentes e permitindo uma conversa geral sobre o time, mantendo a persona de um assistente de fãs dedicado.

A aplicação combina tecnologias de desenvolvimento web (Flask, HTML, CSS, JavaScript), web scraping para dados dinâmicos (escalação de jogadores via HLTV), consumo de feeds RSS (notícias via Google News) e interação com um Modelo de Linguagem Grande (LLM) - Google Gemini - para processamento de linguagem natural e geração de respostas contextuais e engajadoras.

## 2. Requisitos do Sistema

Com base na análise do código e do objetivo do projeto, podemos definir os seguintes requisitos funcionais e não funcionais:

### 2.1. Requisitos Funcionais (RF)

* **RF01:** O sistema deve fornecer uma interface web de chat para interação do usuário.
* **RF02:** O sistema deve permitir que o usuário envie mensagens de texto através da interface.
* **RF03:** O sistema deve identificar perguntas sobre a escalação ("escalacao", "lineup", etc.) e responder com a lista atual de jogadores da FURIA, obtida via web scraping do site HLTV.org.
* **RF04:** O sistema deve identificar perguntas sobre notícias ("noticia", "noticias", etc.) e responder com os títulos e links das últimas notícias relacionadas à FURIA CS2, obtidas via feed RSS do Google News.
* **RF05:** O sistema deve utilizar o LLM Google Gemini para gerar respostas a perguntas gerais não cobertas pelos RF03 e RF04, mantendo a persona definida (assistente de fãs da FURIA CS2).
* **RF06:** O sistema deve formatar as respostas de forma adequada para exibição na interface de chat (HTML).
* **RF07:** O sistema deve prover um mecanismo para iniciar o servidor web.
* **RF08:** O sistema deve tentar abrir a interface web no navegador padrão do usuário ao ser iniciado.
* **RF09:** O sistema deve permitir o encerramento controlado do servidor (via endpoint `/shutdown`).
* **RF10:** O sistema deve solicitar ao LLM um comentário adicional ao fornecer a escalação, baseado na pergunta do usuário.

### 2.2. Requisitos Não Funcionais (RNF)

* **RNF01 (Usabilidade):** A interface do chat deve ser simples, intuitiva e responsiva.
* **RNF02 (Desempenho):** As respostas do chatbot devem ser fornecidas em tempo hábil. (Nota: Latência pode ser introduzida por chamadas de rede ao HLTV, Google News e API Gemini).
* **RNF03 (Confiabilidade/Disponibilidade):** A funcionalidade do chatbot depende da disponibilidade e da estrutura dos serviços externos (HLTV.org, Google News, Google AI API). Falhas nesses serviços podem impactar a disponibilidade de certas respostas. A estrutura do site HLTV pode mudar, quebrando o scraping.
* **RNF04 (Manutenibilidade):** O código deve ser organizado e legível. A separação da lógica de scraping (`web_scraping.py`) contribui para isso. O uso de um `requirements.txt` facilita a gestão de dependências.
* **RNF05 (Portabilidade):** O backend (Python/Flask) deve ser executável em ambientes que suportem Python 3, conforme especificado pelas dependências.

## 3. Arquitetura e Design

### 3.1. Diagrama de Casos de Uso Simplificado

**Descrição:** O usuário interage com o frontend web. O backend Flask recebe as mensagens, identifica a intenção e, dependendo do caso, utiliza módulos de Web Scraping (para escalação), Feed Parsing (para notícias) ou o Cliente LLM (para conversas gerais e comentários) para buscar/gerar a informação. Ele pode precisar acessar serviços externos como HLTV, Google News e a API do Google AI. A resposta formatada é então enviada de volta ao frontend.

### 3.2. Tecnologias e Bibliotecas Utilizadas

* **Backend:**
    * **Python 3:** Linguagem de programação principal.
    * **Flask (`flask>=3.1.0`):** Microframework web para criar o servidor backend, rotear requisições HTTP e renderizar a interface inicial.
    * **Google Generative AI SDK (`google-genai>=1.11.0`):** Biblioteca oficial para interagir com a API do Google Gemini, permitindo enviar prompts, gerenciar histórico (implicitamente pelo objeto `chat`) e receber respostas do LLM.
    * **Beautiful Soup 4 (`beautifulsoup4>=4.10.0`):** Biblioteca para parsing de HTML e XML. Utilizada em `web_scraping.py` para extrair os nomes dos jogadores da página HTML do HLTV.
    * **Feedparser (`feedparser>=6.0.11`):** Biblioteca para fazer o parsing de feeds RSS e Atom, usada para obter e processar as notícias do Google News.
    * **Urllib (`urllib.request`, `urllib.parse`):** Módulos nativos do Python utilizados para abrir URLs (fazer requisições HTTP básicas) e codificar parâmetros de URL (para a busca no Google News).
    * **Bibliotecas Padrão:** `os`, `threading`, `time`, `webbrowser` para funcionalidades do sistema operacional, execução paralela leve (abrir browser), pausas e controle do navegador.
* **Frontend:**
    * **HTML5 (`web/index.html`):** Estrutura da página de chat.
    * **CSS3 (`web/style.css`):** Estilização da interface do chat, definindo layout, cores e aparência.
    * **JavaScript (`web/chat.js`):** Lógica do lado do cliente para manipular o DOM, capturar o input do usuário, enviar requisições assíncronas (Fetch API) para o endpoint `/api/chat` do backend Flask, e exibir as mensagens do usuário e do bot na interface.
* **Ambiente e Execução:**
    * **Bash Script (`run.sh`):** Automatiza a criação/ativação de ambiente virtual (`venv`), instalação de dependências (`pip`) e execução do servidor Flask.
    * **pip:** Gerenciador de pacotes Python.
    * **venv:** Ferramenta para criação de ambientes virtuais Python.
    * **(Listado mas não usado em `run.sh`) Gunicorn (`gunicorn>=20.1.0`):** Servidor WSGI HTTP para Python, frequentemente usado para deploy de aplicações Flask/Django em produção (alternativa ao servidor de desenvolvimento do Flask).
    * **(Listado mas não usado no código) `googlesearch-python>=1.3.0`:** Biblioteca para realizar buscas no Google (não utilizada na lógica final apresentada).

### 3.3. Estrutura do Projeto

```
Challenge1Linux/
├── chat.py             # Arquivo principal da aplicação Flask e lógica do chat
├── web_scraping.py     # Módulo com funções de web scraping e feed parsing
├── requirements.txt    # Lista de dependências Python
├── run.sh              # Script para configurar e executar a aplicação
└── web/                  # Pasta com arquivos do frontend
    ├── index.html      # Estrutura HTML da página
    ├── style.css       # Estilos CSS
    ├── chat.js         # Lógica JavaScript do cliente
    └── imgs/           # (Implícito pelo CSS) Pasta para imagens
        └── Fundofuria1.jpg # Imagem de fundo
```

## 4. Análise de Alternativas e Decisões de Design

Durante o desenvolvimento ou em uma evolução deste projeto, diversas alternativas poderiam ser consideradas:

* **Web Scraping:**
    * **Robustez:** Se o HLTV utilizasse JavaScript para carregar dados dinamicamente, `BeautifulSoup` sozinho não seria suficiente. Ferramentas como `Selenium` (automatiza um navegador real) ou `Playwright` seriam necessárias, embora adicionem complexidade e dependências.
    * **Framework:** Para scraping mais complexo ou em maior escala, o framework `Scrapy` oferece uma estrutura mais completa com pipelines, middlewares e gerenciamento de requisições assíncronas.
* **Orquestração da Lógica do Chat:**
    * **Fluxo Atual:** A lógica em `chat.py` usa condicionais (`if/elif/else`) para direcionar a requisição (Scraping, News, LLM). Funciona para poucos casos, por simplicidade foi utilizado assim.
    * **LangGraph/LangChain:** Essas bibliotecas permitiriam modelar o fluxo de decisão como um grafo de estados. Cada nó poderia representar uma ação (Analisar Intenção, Buscar Notícias, Buscar Escalação, Chamar LLM), e as transições seriam definidas com base no estado atual (intenção do usuário, dados já coletados). Isso melhora a modularidade e a visualização do fluxo para lógicas mais complexas.
    * **CrewAI:** Abordagem focada em agentes autônomos. Poderíamos definir: um `Agente Analista` (identifica a intenção), um `Agente ScraperHLTV` (com ferramenta para buscar escalação), um `Agente RepórterDeNotícias` (com ferramenta para buscar notícias), e um `Agente FãDaFuria` (interage com o LLM para respostas gerais e comentários). A `Crew` orquestraria a colaboração desses agentes para responder ao usuário. Ideal para tarefas que se beneficiam de especialização e delegação.
    * **Function Calling (Gemini Tools):** Em vez do código Python decidir *sempre* qual ferramenta usar, poderíamos definir as funções de scraping e busca de notícias como "Tools" para o Gemini. O LLM, ao receber a pergunta, poderia *solicitar* a execução da ferramenta apropriada. O código Python executaria a função e devolveria o resultado para o LLM gerar a resposta final. Isso torna a interação mais dinâmica e dependente da capacidade do LLM de escolher a ferramenta correta.
* **Framework Web Backend:**
    * **Flask:** Escolha atual, ótimo para microserviços e aplicações simples/médias. Flexível.
    * **Django:** Framework "batteries-included", com ORM, admin, etc. Mais opinativo, pode ser excessivo para este projeto, mas excelente para aplicações maiores e mais complexas.
    * **FastAPI:** Framework moderno baseado em type hints Python, focado em performance e APIs assíncronas. Seria uma ótima escolha se a performance e operações I/O-bound (como chamadas de API e scraping) fossem críticas e se desejasse usar `asyncio`.
* **LLM:**
    * **Google Gemini (Flash):** Modelo utilizado, bom equilíbrio entre performance e custo. Outros modelos Gemini (Pro) ou de outros provedores (OpenAI GPT, Anthropic Claude, etc.) poderiam ser testados para avaliar diferenças em qualidade de resposta, aderência à persona e custo.
* **Deployment:**
    * **Servidor de Desenvolvimento Flask:** Usado atualmente (`app.run`). Não recomendado para produção.
    * **Gunicorn/uWSGI:** Servidores WSGI robustos para rodar aplicações Python em produção, geralmente por trás de um proxy reverso como Nginx. `Gunicorn` está no `requirements.txt`.
    * **Containerização (Docker):** Empacotar a aplicação e suas dependências em um container Docker facilitaria o deploy em diferentes ambientes e a escalabilidade.

## 5. Instruções de Instalação e Execução

Estas instruções assumem um ambiente Linux/Unix-like com Python 3 e `pip` instalados.

1.  **Clone o Repositório:**
    ```bash
    # git clone [URL_DO_SEU_REPOSITORIO]
    cd Challenge1Linux
    ```

2.  **Execute o Script `run.sh`:**
    Este script automatiza a criação do ambiente virtual, instalação de dependências e inicialização do servidor.
    ```bash
    bash run.sh
    ```
    * O script criará uma pasta `.venv`.
    * Instalará as bibliotecas listadas em `requirements.txt`.
    * Iniciará o servidor Flask na porta 8000 (`http://localhost:8000` ou `http://0.0.0.0:8000`).

3.  **Acesse a Aplicação:**
    O script tentará abrir automaticamente `http://localhost:8000` no seu navegador padrão. Se não abrir, navegue manualmente para este endereço.

4.  **Interaja com o Chatbot:** Use a interface web para conversar com o chatbot.

5.  **Parar o Servidor:**
    * Você pode parar o servidor pressionando `Ctrl + C` no terminal onde `run.sh` está executando.
    * Alternativamente, o endpoint `/shutdown` pode ser acionado (o `chat.js` tenta fazer isso ao fechar a aba/navegador usando `navigator.sendBeacon`).


## 6. Pontos de Melhoria e Próximos Passos

* **Tratamento de Erros:** Implementar tratamento de erros mais robusto para falhas de rede (ao fazer scraping ou chamar APIs), parsing de HTML/RSS e respostas inesperadas da API do LLM. Exibir mensagens de erro mais informativas para o usuário.
* **Robustez do Scraping:** Monitorar a estrutura do HLTV. Se mudar frequentemente, considerar alternativas (API não oficial, se existir e for confiável) ou implementar o scraping com `Selenium`/`Playwright` se o conteúdo for dinâmico.
* **Cache:** Implementar cache para dados externos (escalação, notícias) para reduzir a latência e o número de requisições a serviços externos, definindo um tempo de expiração apropriado (ex: a cada 30 minutos).
* **Assincronicidade:** Converter as operações de I/O (chamadas de API, scraping) para assíncronas usando `asyncio` e bibliotecas como `aiohttp` (ou migrar para FastAPI) pode melhorar o desempenho e a capacidade de lidar com múltiplos usuários simultaneamente.
* **Testes:** Adicionar testes unitários (para funções de scraping, parsing, lógica do Flask) e testes de integração para garantir a funcionalidade e facilitar refatorações.
* **Interface do Usuário:** Melhorar a interface com indicadores de "digitando...", melhor formatação de mensagens, talvez opções de feedback.
* **Monitoramento e Logging:** Implementar logging mais detalhado para acompanhar o fluxo de requisições, identificar erros e monitorar o desempenho da aplicação em um ambiente de produção.
* **Deployment:** Preparar a aplicação para deploy usando Gunicorn/uWSGI e Nginx, preferencialmente dentro de containers Docker.


## 7. Execução no Windows
Para Windows, temos o arquivo .exe do chat para facilitar a execução. Feito com a biblioteca Pyinstaller.

## 8. Conclusão

O projeto Chatbot FURIA FANS demonstra a integração de diversas tecnologias para criar uma aplicação web interativa e útil. Ele utiliza web scraping e parsing de RSS para obter dados dinâmicos e uma LLM para fornecer respostas contextuais e engajadoras, tudo orquestrado por um backend Flask e apresentado através de uma interface web simples. A análise de requisitos, design, alternativas e pontos de melhoria reflete uma abordagem alinhada com práticas de Engenharia de Software, mostrando potencial para evoluções futuras e aplicação em cenários mais complexos.
