from enum import Enum
from collections import namedtuple
import re

class Transação(object):
	"""Estados possíveis em que uma transação pode estar"""
	(INICIADA, LENDO, COMMITED) = (1, 2, 3)
	"""docstring for Transação"""
	def __init__(self, identificador, operações):
		super(Transação, self).__init__()
		self.identificador = identificador
		self.operações = operações
		self.estado = self.INICIADA
		self.conjunto_leitura = set()
		self.conjunto_escrita = set()

	def primeiro_teste(Ti,Tj):
		# Transaction Tj completa sua fase de escrita antes que Ti começou sua
		# fase de leitura
		if (Tj.timestamp_commit < Ti.timestamp_leitura):
			return True
		else:
			return False

	def segundo_teste(Ti, Tj):
		# Ti começa a sua fase de escrita depois que Tj completa sua fase de
		# escrita e o conjunto de leitura de Ti não tem intersecção com o
		# conjunto de escrita de Tj
		if (Ti.conjunto_leitura.isdisjoint(Tj.conjunto_leitura)):
			return True
		else:
			return False

	def terceiro_teste(Ti, Tj):
		# A união do conjunto de leitura e escrita de Ti não tem intersecção
		# com o conjunto de escrita de Tj e Tj completa sua fase de leitura antes de Ti.
		if (Ti.conjunto_leitura.isdisjoint(Tj.conjunto_escrita) and Ti.conjunto_escrita.isdisjoint(Tj.conjunto_escrita)):
			return True
		else:
			return False
		

	def validar(Ti,timestamp,comitadas):
		teste = lambda Tj: Ti.primeiro_teste(Tj) or Ti.segundo_teste(Tj) or Ti.terceiro_teste(Tj)
		validada = all(map(teste,comitadas))
		if (validada):
			Ti.timestamp_commit = timestamp
			Ti.estado = Ti.COMMITED
		return validada

	def ler_do_arquivo(caminho):
		arquivo = open(caminho,"r");
		retorno = []
		for line in arquivo:
			identificador = int(line.split(":")[0][1:])
			operações = re.findall("(\S+?)\((\S+?)\)",line.split(":")[1])
			operações = list(map(Operação._make,operações))
			retorno.append(Transação(identificador,operações))
		return retorno

	def iniciar_leitura(self,timestamp):
		self.estado = self.LENDO
		self.timestamp_leitura = timestamp
		self.numero_operações = 0

	def inserir_operação(self,operação):
		"""Insere a operação no conjunto apropriado. Retorna True se todas as operações daquela transação forem realizadas, assinalando a hora de dar commit"""
		if (operação.op == "w"):
			self.conjunto_leitura.add(operação.objeto)
		else:
			self.conjunto_escrita.add(operação.objeto)

		self.numero_operações = self.numero_operações + 1
		if (self.numero_operações == len(self.operações) ):
			return True
		else:
			return False

	def reiniciar_transação(self):
		"""Reincia a transação"""
		self.estado = self.INICIADA
		self.conjunto_leitura.clear()
		self.conjunto_escrita.clear()



Operação = namedtuple("Operação",['op','objeto'])