# sera que é melhor fazer uma classe memória e uma cpu ou so fazer uma lista pra memoria??
class Memoria:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.memoria = [0] * tamanho 

    def escrever (self, endereco, dado):
        '''Função que recebe um endereço e um dado, e vai armazenar esse dado no endereço recebido'''
    
    def ler (self, endereco):
        '''Vai receber um endereço e vai retornar o dado que tá armazenado la
        '''

class CPU:
    def __init__(self):
        self.MAR = 0 #armazena o endereço
        self.PC = 0 #ponteiro 
        self.IR = "" #armazena a instrução, é um int ou uma string?
        self.MBR = "" #armazena o dado a ser lido ou escrito    
        
    # aqui fica o ciclo de instrução de fato

class ULA:
    def __init__(self):
        self.AC = 0 #acumulador
        self.C = 0 #registrador de carry, (1 se houve carry, -2 se não)
        self.Z = 0 #registrador de zero (-1 resultado negativo; 0 resultado zero; 1 resultado positivo)
        self.M = 0 #Multiplicador
        self.R = 0 #Resto

    # Na ula a gente precisa fazer todas as operações será? as lógicas e as matemáticas?

def main():
    '''Tem que fazer abrir arquivo né, a gente faz outro arquivo pra ter so a main ou deixa tudo corrido aqui?'''

if __name__ == "__main__":
    main()