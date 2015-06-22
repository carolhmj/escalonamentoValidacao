from enum import Enum
from collections import namedtuple
import re

class Transação(object):
	"""docstring for Transação"""
	# Estados possíveis em que uma transação pode estar
	(INICIADA, LENDO, COMMITED) = (1, 2, 3)

	def __init__(self, identificador, operações):
		super(Transação, self).__init__()
		self.identificador = identificador
		self.operações = operações
		self.estado = self.INICIADA
		self.conjunto_leitura = set()
		self.conjunto_escrita = set()

		self.timestamp_commit = None
		self.timestamp_leitura = None

		for op in operações:
			if   op.op == "w":
				self.conjunto_escrita.add(op.objeto)
			elif op.op == "r":
				self.conjunto_leitura.add(op.objeto)

	def __repr__(self):
		out = "Transação("+repr(self.identificador)+",[\""
		for op in self.operações:
			out+=op.op+"("+op.objeto+")"
		out += "\"])"
		return out

	def __str__(self):
		out = "T"+str(self.identificador)+":"
		for op in self.operações:
			out+=op.op+"("+op.objeto+")"
		return out

	def nome(self):
		return "T"+str(self.identificador)

	def primeiro_teste(Ti,Tj):
		"""Transação Tj completa sua fase de escrita antes que Ti começou sua
		fase de leitura """
		#print ("Primeiro Teste")
		#print (Tj.nome()+".timestamp_commit < "+Ti.nome()+".timestamp_leitura")
		#print (str(Tj.timestamp_commit)+"<"+str(Ti.timestamp_leitura))
		#print ((Tj.timestamp_commit)<(Ti.timestamp_leitura))
		return Tj.timestamp_commit < Ti.timestamp_leitura

	def segundo_teste(Ti, Tj):
		"""Ti começa a sua fase de escrita depois que Tj completa sua fase de
		escrita e o conjunto de leitura de Ti não tem intersecção com o
		conjunto de escrita de Tj"""
		#print ("\nSegundo Teste")
		#print (Ti.nome()+".conjunto_leitura.isdisjoint("+Tj.nome()+".conjunto_escrita)")
		#print (str(Ti.conjunto_leitura)+".isdisjoint("+str(Tj.conjunto_escrita)+")")
		#print (Ti.conjunto_leitura.isdisjoint(Tj.conjunto_escrita))
		return Ti.conjunto_leitura.isdisjoint(Tj.conjunto_escrita)

	def terceiro_teste(Ti, Tj):
		"""A união do conjunto de leitura e escrita de Ti não tem intersecção
		com o conjunto de escrita de Tj e Tj completa sua fase de leitura antes
		de Ti."""
		x = Ti.conjunto_leitura.isdisjoint(Tj.conjunto_escrita) and \
		    Ti.conjunto_escrita.isdisjoint(Tj.conjunto_escrita)
		#print("\nTerceiro Teste")
		#print(Ti.nome()+".conjunto_leitura.isdisjoint("+Tj.nome()+".conjunto_escrita) and \n"+
		#      Ti.nome()+".conjunto_escrita.isdisjoint("+Tj.nome()+".conjunto_escrita)")
		#print(str(Ti.conjunto_leitura)+".isdisjoint("+str(Tj.conjunto_escrita)+") and \n"+
		#      str(Ti.conjunto_escrita)+".isdisjoint("+str(Tj.conjunto_escrita)+")")
		#print(x)
		return x

	def validar(Ti,timestamp,comitadas):
		teste = lambda Tj: Ti.primeiro_teste(Tj) or \
		                   Ti.segundo_teste(Tj)  or \
		                   Ti.terceiro_teste(Tj)

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

	def próxima_operação(self):
		"""Leva a transação par a próxima operação.
		Retorna True se todas as operações daquela transação forem realizadas,
		assinalando a hora de dar commit"""

		self.numero_operações = self.numero_operações + 1
		return self.numero_operações == len(self.operações)

	def reiniciar_transação(self):
		"""Reincia a transação"""
		self.estado = self.INICIADA

Operação = namedtuple("Operação",['op','objeto'])
