import os
import discord
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

modelo_gemini = "gemini-1.5-flash"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
  "temperature": 1,
  "response_mime_type": "text/plain"
}
prompt_sistema = """
Você é um robô de atendimento da empresa Hare Express, uma empresa de entrega inovadora que se destaca pela sua velocidade e eficiência.
Você deve responder as perguntas dos clientes de maneira educada e objetiva.
A resposta deve ter no máximo 1000 caracteres.
"""
gemini = genai.GenerativeModel(
  model_name = modelo_gemini,
  generation_config=generation_config,
  system_instruction = prompt_sistema)

intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
  print(f'Logado como {discord_client.user}!')

@discord_client.event
async def on_message(message):
  if message.author == discord_client.user:
    return

  nome_cliente = message.author
  mensagem_cliente = message.content
  
  tamanho_mensagem_cliente = len(mensagem_cliente)
  print(tamanho_mensagem_cliente)
  
  print(f'Mensagem de {nome_cliente}: {mensagem_cliente}')

  channel = discord_client.get_channel(message.channel.id)
  
  resposta = gemini.generate_content(f"""
                                     Nome do cliente: {nome_cliente}
                                     Mensagem do cliente: {mensagem_cliente}
                                     """)
  mensagem_resposta = resposta.text
  print(len(mensagem_resposta))
  print(mensagem_resposta)
  await channel.send(mensagem_resposta)

discord_client.run(os.getenv('DISCORD_CLIENT_TOKEN'))
