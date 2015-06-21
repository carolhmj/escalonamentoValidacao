from transação import Transação
from transação import Operação
import re
from collections import namedtuple
import os
import sys

class Gerenciador(object):

	def __init__(self, arquivo_transacoes):
		super(Gerenciador, self).__init__()
		self.lista_transacoes = Transação.ler_do_arquivo(arquivo_transacoes)

	def ler_história():
		história = input()
		história = re.findall("(\S+?)(\d+)\((\S+?)\)",hist)
		história = map(lambda p: (p[0],int(p[1]),p[2]), sequence)
		história = list(map(OperaçãoGerenciador._make,história))
		return história

	def escrever_historia(história, arquivo):
		for operação in história:
			arquivo.write(operação.op + operação.transação + "(" + operação.objeto + ")")


	def executar(self, arquivo_saida):
		história_inicial = Gerenciador.ler_história()
		#Inicialmente a história de saída é igual a história inicial, isso pode mudar quando retirarmos transações dela
		história_saída = história_inicial

		#arquivo = open(arquivo_saida,'w')
		arquivo = sys.stdout;
		arquivo.write("Schedule de Entrada: ")
		Gerenciador.escrever_historia(história_inicial, arquivo)

		timestamp = 1
		lista_commited = []
		lista_cancelada = []
		for operação in história_inicial:
			transação = self.lista_transacoes[operação.transação-1]

			if (transação.estado == Transação.INICIADA):
				transação.iniciar_leitura(timestamp)

			if (transação.inserir_operação(Operação(operação.op, operação.objeto))):
				if (transação.validar(timestamp,lista_commited)):
					lista_commited.append(transação)
				else:
					transação.reiniciar_transação()
					história_saída = filter(lambda x: x.transação != transação.identificador, história_saída)
					lista_cancelada.append(transação)

			timestamp = timestamp + 1

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
