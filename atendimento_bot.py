import os
from dotenv import load_dotenv
import discord
import google.generativeai as genai
from correios_rastreamento import busca_info_rastreamento

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

faq_file = genai.upload_file(path='faq-hare-express.pdf')

modelo_gemini = "gemini-1.5-flash"
generation_config = {
  "temperature": 0,
  "response_mime_type": "text/plain"
}
prompt_sistema = """
Você é um robô de atendimento da empresa Hare Express, uma empresa de entrega inovadora que se destaca pela rapidez e eficiência.
Você deve responder de maneira educada, objetiva e formal.
Apenas responda perguntas relativas aos serviços da Hare Express.
Utilize apenas as informações contidas no PDF em anexo.
Caso a pergunta não seja relacionada a algum serviço da Hare Express, educadamente se negue a responder.
Toda vez que você encontrar uma string no formato 13 caracteres alfanuméricos, sendo 2 letras, 9 números e 2 letras trata-se de um código de rastreamento de objeto que pode ser respondido pela função 'busca_info_rastreamento'. Exemplo de código de objeto: JN732917265BR.
"""
gemini = genai.GenerativeModel(
  model_name = modelo_gemini,
  generation_config=generation_config,
  system_instruction=prompt_sistema,
  tools=[busca_info_rastreamento]
)

intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
  print(f'Logado como {discord_client.user}')

@discord_client.event
async def on_message(message):
  if message.author == discord_client.user:
    return

  nome_cliente = message.author
  mensagem_client = message.content
  print(f'Mensagem de {nome_cliente}: {mensagem_client}' )
  
  id_canal = message.channel.id
  canal = discord_client.get_channel(id_canal)
  
  prompt = f"""
            Nome do Cliente: {nome_cliente}
            Mensagem do Cliente: {mensagem_client}
            """

  chat = gemini.start_chat(enable_automatic_function_calling=True)
  resposta = chat.send_message([prompt, faq_file])

  print(resposta)

  mensagem_bot = resposta.text

  await canal.send(mensagem_bot)

discord_client.run(os.getenv('DISCORD_CLIENT_TOKEN'))