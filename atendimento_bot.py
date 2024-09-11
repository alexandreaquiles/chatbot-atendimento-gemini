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

faq_file = genai.upload_file(path='faq-hare-express.pdf')

prompt_sistema = """
Você é um robô de atendimento da empresa Hare Express, uma empresa de entrega inovadora que se destaca pela rapidez e eficiência.
Você deve responder de maneira educada, objetiva e formal.
Apenas responda perguntas relativas aos serviços da Hare Express.
Utilize apenas as informações contidas no PDF em anexo.
Caso a pergunta não seja relacionada a algum serviço da Hare Express, educadamente se negue a responder.
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
  
  resposta = gemini.generate_content([f"""
                                     Nome do cliente: {nome_cliente}
                                     Mensagem do cliente: {mensagem_cliente}
                                     """, faq_file])
  mensagem_resposta = resposta.text
  print(len(mensagem_resposta))
  print(mensagem_resposta)
  await channel.send(mensagem_resposta)

discord_client.run(os.getenv('DISCORD_CLIENT_TOKEN'))
