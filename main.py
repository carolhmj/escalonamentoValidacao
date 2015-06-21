from gerenciador import Gerenciador

def main():

	arquivo_transações = input("Entre com o arquivo de descrição das transações: ")

	ger = Gerenciador(arquivo_transações)

	sair = False

	while not sair:

		arquivo_história = input("Entre com o arquivo com a história das transações. Caso deseje inseri-las a \
			partir do terminal, escreva \"stdin\": ")
		arquivo_saída = input("Entre com o arquivo com a saída da execução da história. Caso deseje vê-la no \
			terminal, escreva \"stdout\": ")

		ger.executar(arquivo_história, arquivo_saída)

		print("")
		encerrar = input("Deseja sair? (s/n) ")
		while (encerrar != "s" and encerrar != "n"):
			encerrar = input("Deseja sair? (s/n) ")
		if (encerrar == "s"):
			sair = True
		else:
			sair = False

if __name__ == '__main__':
	main()