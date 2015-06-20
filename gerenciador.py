from transação import Transação
from transação import Operação
import re
from collections import namedtuple
import os

class Gerenciador(object):

	def __init__(self, arquivo_transacoes):
		super(Gerenciador, self).__init__()
		self.lista_transacoes = Transação.ler_do_arquivo(arquivo_transacoes)

	def ler_história(arquivo_história):
		arquivo = open(arquivo_história,'r')
		história = re.findall("(\S)(\d+?)\((\S+?)\)",arquivo.read())
		história = list(map(OperaçãoGerenciador._make,história))
		arquivo.close()
		return história

	def escrever_historia(história, arquivo):
		for operação in história:
			arquivo.write(operação.op + operação.transação + "(" + operação.objeto + ")")
		

	def executar(self, arquivo_história, arquivo_saida):
		história_inicial = Gerenciador.ler_história(arquivo_história)
		#Inicialmente a história de saída é igual a história inicial, isso pode mudar quando retirarmos transações dela
		história_saída = história_inicial

		os.remove(arquivo_saida)
		arquivo = open(arquivo_saida,'a+')
		arquivo.write("Schedule de Entrada: ")
		Gerenciador.escrever_historia(história_inicial, arquivo)

		timestamp = 1
		lista_commited = []
		lista_cancelada = []
		for operação in história_inicial:

			transação = self.lista_transacoes[int(operação.transação)-1]
			if (transação.estado == Transação.INICIADA):
				transação.iniciar_leitura(timestamp)
			if (transação.inserir_operação(Operação(operação.op, operação.objeto))):

				if (transação.validar(timestamp,lista_commited)):
					lista_commited.append(transação)
				else:
					transação.reiniciar_transação()
					história_saída = filter(lambda x: x.transação != str(transação.identificador), história_saída)
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
