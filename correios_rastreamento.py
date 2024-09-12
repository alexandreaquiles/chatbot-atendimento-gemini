import urllib3
import logging
from urllib3.util import Retry

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("urllib3")

http = urllib3.PoolManager()

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[413, 429, 500, 502, 503, 504],
    raise_on_status=False
)

def log_retry_attempt(method, url, error, _):
    logger.debug(f"Retrying {method} request to {url} due to {error}")

retries._is_retry = log_retry_attempt

def busca_info_rastreamento(codigo_rastreamento:str):
  """Busca informações do rastreamento de objetos e encomendas da Hare Express de qualquer localidade do Brasil a partir do código de rastreamento.

  Args:
      codigo_rastreamento: Código de rastreamento obtido no momento da postagem da encomenda.
      O código de Rastreamento é composto de 13 dígitos, começando com 2 letras seguidas de 9 letras e de mais 2 letras.
      Exemplos: JN732917265BR, QS244376229BR, OY313609204BR
      
  Returns:
      Um dicionário Python contendo o código de rastreamento, um array de eventos contendo cada status da entrega, além de outras informações.
      Caso o objeto não seja encontrado, o array de eventos estará vazio.

      Exemplo de objeto entregue: {'codigo': 'JN732917265BR', 'host': 'rd', 'eventos': [{'data': '23/07/2024', 'hora': '11:34', 'local': 'Criciuma / SC', 'status': 'Objeto entregue ao destinatário', 'subStatus': ['Local: Unidade de Distribuição - Criciuma / SC']}, {'data': '23/07/2024', 'hora': '07:31', 'local': 'Criciuma / SC', 'status': 'Objeto saiu para entrega ao destinatário', 'subStatus': ['Local: Unidade de Distribuição - Criciuma / SC']}, {'data': '11/07/2024', 'hora': '13:01', 'local': 'Caraguatatuba / SP', 'status': 'Objeto postado', 'subStatus': ['Local: Agência dos Correios - Caraguatatuba / SP']}], 'time': 0.071, 'quantidade': 3, 'servico': 'MALA DIRETA POSTAL ESPECIAL', 'ultimo': '2024-07-23T14:34:00.000Z'}
      Exemplo de objeto encaminhado: {'codigo': 'AK390407941BR', 'host': 'lt', 'eventos': [{'data': '10/09/2024', 'hora': '10:37', 'local': 'Varzea Grande / MT', 'status': 'Objeto encaminhado', 'subStatus': ['Origem: Unidade de Tratamento - Varzea Grande / MT', 'Destino: Unidade de Distribuição - Porto Velho / RO']}, {'data': '05/09/2024', 'hora': '12:55', 'local': 'Blumenau / SC', 'status': 'Objeto encaminhado', 'subStatus': ['Origem: Unidade de Tratamento - Blumenau / SC', 'Destino: Unidade de Tratamento - Varzea Grande / MT']}, {'data': '04/09/2024', 'hora': '14:28', 'local': 'Florianopolis / SC', 'status': 'Objeto encaminhado', 'subStatus': ['Origem: Agência dos Correios - Florianopolis / SC', 'Destino: Unidade de Tratamento - Blumenau / SC']}, {'data': '04/09/2024', 'hora': '13:41', 'local': 'Florianopolis / SC', 'status': 'Objeto postado', 'subStatus': ['Local: Agência dos Correios - Florianopolis / SC']}], 'time': 0.737, 'quantidade': 4, 'servico': '', 'ultimo': '2024-09-10T13:37:00.000Z'}
      Exemplo de objeto não encontrado: {'codigo': 'XX111111111YY', 'host': 'lt', 'eventos': [], 'time': 0.733, 'quantidade': 0, 'servico': 'REMESSA INTERNACIONAL'}
  """

  print(f'Vai rastrear o objeto: {codigo_rastreamento}')

  url = f"https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={codigo_rastreamento}"

  resp = http.request("GET", url, retries=retries)

  print(f'Rastreou o objeto {codigo_rastreamento}')
  print(f'HTTP Status: {resp.status}')

  if resp.status == 200:
      return resp.json()

  return resp.data

