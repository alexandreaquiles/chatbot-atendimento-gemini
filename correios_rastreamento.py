import urllib3
from urllib3.util import Retry
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("urllib3")

http = urllib3.PoolManager()

retries = Retry(
  total=5,
  backoff_factor=1,
  raise_on_status=False,
  status_forcelist=[413, 429, 500, 502, 503, 504]
)
def log_retry_attempt(method, url, error, _):
  logger.debug(f"Retrying {method} request to {url} due to {error}")

retries._is_retry = log_retry_attempt

def busca_info_rastreamento(codigo_objeto: str):
  """Busca informações de rastreamento de objetos e encomendas postados na Hare Express de qualquer localidade do Brasil e do mundo a partir do código de objeto.

  Args:
    codigo_objeto: Código de rastreamento do objeto obtido pelo cliente no momento da postagem ou compra.
    O código tem uma formatação com o total de 13 caracteres alfanuméricos, sendo 2 letras, 9 números, finalizando com 2 letras.
    As duas letras finais representam o país de origem.
    Exemplos: JN732917265BR, QS244376229BR, OY313609204BR

  Returns:
    Um dicionário Python contendo o código do objeto, um array de eventos contendo cada status da entrega, além de outras informações.
    Caso o objeto não seja encontrado, o array de eventos estará vazio.
    Exemplo de um objeto com rastreamento: {'codigo': 'JN732917265BR', 'host': 'rd', 'eventos': [{'data': '23/07/2024', 'hora': '11:34', 'local': 'Local: Unidade de Distribuição - Criciuma / SC', 'status': 'Objeto entregue ao destinatário', 'subStatus': []}, {'data': '23/07/2024', 'hora': '07:31', 'local': 'Local: Unidade de Distribuição - Criciuma / SC', 'status': 'Objeto saiu para entrega ao destinatário', 'subStatus': []}, {'data': '11/07/2024', 'hora': '13:01', 'local': 'Local: Agência dos Correios - Caraguatatuba / SP', 'status': 'Objeto postado', 'subStatus': []}], 'time': 0.072, 'quantidade': 3, 'servico': 'MALA DIRETA POSTAL ESPECIAL', 'ultimo': '2024-07-23T14:34:00.000Z'}
  """

  print(f"Vai rastrear o objeto {codigo_objeto}")
  
  url = f"https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={codigo_objeto}"

  response = http.request("GET", url, retries=retries)
  
  print(f"Rastreou o objeto {codigo_objeto} e obteve {response.status}")

  
  if response.status == 200:
    return response.json()
  
  return response.data
