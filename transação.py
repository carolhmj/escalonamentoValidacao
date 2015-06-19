from enum import Enum
from collections import namedtuple
import re

class Transação(object):
	"""docstring for Transação"""
	def __init__(self, identificador, operações):
		super(Transação, self).__init__()
		self.identificador = identificador
		self.operações = operações
	def ler_do_arquivo(caminho):
		arquivo = open(caminho,"r");
		retorno = []
		for line in arquivo:
			identificador = line.split(":")[0]
			operações = re.findall("(\S+?)\((\S+?)\)",line.split(":")[1])
			operações = list(map(Operação._make,operações))
			retorno.append(Transação(identificador,operações))
		return retorno


Operação = namedtuple("Operação",['op','objeto'])