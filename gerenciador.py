from transação import Transação
from transação import Operação
from collections import namedtuple
import os
import sys
import re

class Gerenciador(object):

	def __init__(self, arquivo_transacoes):
		super(Gerenciador, self).__init__()
		self.lista_transacoes = Transação.ler_do_arquivo(arquivo_transacoes)

	def ler_história(arquivo_entrada):
		if arquivo_entrada == "stdin":
			história = input("Insira a história de entrada: ")
		else:
			arquivo  = open(arquivo_entrada,'r')
			história = arquivo.readline()
			arquivo.close()

		história = re.findall("(\S+?)(\d+)\((\S*?)\)",história)
		história = map(lambda p: (p[0],int(p[1]),p[2]), história)
		história = list(map(OperaçãoGerenciador._make,história))
		return história

	def escrever_historia(história, arquivo):
		for operação in história:
			arquivo.write(operação.op + str(operação.transação) + "(" + operação.objeto + ")")

	def executar(self,arquivo_entrada,arquivo_saida):
		história_inicial = Gerenciador.ler_história(arquivo_entrada)
		# Inicialmente a história de saída é igual a história inicial,
		# isso pode mudar quando retirarmos transações dela
		história_saída = história_inicial

		if arquivo_saida == "stdout":
			arquivo = sys.stdout;
		else:
			arquivo = open(arquivo_saida,'w')

		arquivo.write("Schedule de Entrada: ")
		Gerenciador.escrever_historia(história_inicial, arquivo)

		timestamp = 1
		lista_commited = []
		lista_cancelada = []
		for operação in história_inicial:
			transação = self.lista_transacoes[operação.transação-1]

			if (transação.estado == Transação.INICIADA):
				transação.iniciar_leitura(timestamp)

			if (transação.próxima_operação()):
				#print("\nValidando: " + str(transação) + ": ",end="\n")
				if (transação.validar(timestamp,lista_commited)):
					#print("Validado")
					lista_commited.append(transação)
				else:
					#print("Abortado")
					transação.reiniciar_transação()
					história_saída = list(filter(lambda x: x.transação != transação.identificador, história_saída))
					lista_cancelada.append(transação)

			timestamp = timestamp + 1

		for transação in lista_cancelada:
			for operação in transação.operações:
				história_saída.append(OperaçãoGerenciador(operação.op, transação.identificador, operação.objeto))

		arquivo.write("\nSchedule de Saída: ")
		Gerenciador.escrever_historia(história_saída, arquivo)
		arquivo.write("\nDeadlock: Não")
		arquivo.write("\nTransações Abortadas: ")
		i = 0
		for l in lista_cancelada:
			arquivo.write("T"+str(l.identificador))
			i = i+1
			if (i<len(lista_cancelada)):
				arquivo.write(", ")
		arquivo.write("\nTransações Efetivadas: ")
		i = 0
		for l in lista_commited:
			arquivo.write("T"+str(l.identificador))
			i = i+1
			if (i<len(lista_commited)):
				arquivo.write(", ")

OperaçãoGerenciador = namedtuple("OperaçãoGerenciador",['op','transação','objeto'])
