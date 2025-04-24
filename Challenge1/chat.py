import openai

chave_api = "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"

openai.api_key = chave_api

def enviar_conversa(mensagem, lista_mensagens=[]):
    
    lista_mensagens.append(
        {"role":"user", "content": mensagem}
        )
    
    resposta = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = lista_mensagens,
    )
    return resposta.choices[0].message.content

lista_mensagens = []
while True:
    texto = input("Digite sua mensagem:")

    if texto == "sair":
        break
    else:
        resposta = enviar_conversa(texto, lista_mensagens)
        lista_mensagens.append({'role': 'user', 'content': resposta})
        print("Chatbot:", resposta)     
        



