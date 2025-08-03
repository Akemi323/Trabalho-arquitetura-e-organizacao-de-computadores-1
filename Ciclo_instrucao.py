#Isadora Dantas Bruchmam (ra140870), João Vitor Bidoia Ângelo(ra139617) e Letícia Akemi Nakahati Vieira (ra140535)
from __future__ import annotations
import os

TAMANHO_PALAVRA_BITS = 40
MAX_VALOR_PALAVRA = 2 ** TAMANHO_PALAVRA_BITS 


class Memoria:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.memoria = [0] * tamanho

    def escrever (self, endereco, dado):
        '''Função que recebe um endereço e um dado, e vai armazenar esse dado no endereço recebido'''
        self.memoria[endereco] = dado
    
    def ler (self, endereco):
        '''Vai receber um endereço e vai retornar o dado que tá armazenado la
        '''
        return self.memoria[endereco]

class CPU:
    def __init__(self, memoria, ula):
        self.registradores = {
            'PC': 0, 'MAR': 0, 'MBR': None, 'IR': None, 'IBR': None,
            'AC': 0, 'C': 0, 'Z': 0, 'MQ': 0, 'R': 0
        }
        self.Ula = ula
        self.memoria = memoria
        self.arquivo_operacao = inicializa() #open("readme.txt", 'r')

    def busca(self):
        ''''''
        # PC vai pro MAR
        self.registradores['MAR'] = self.registradores['PC']

        # Leitura do dado na memória no endereço que o MAR aponta
        self.registradores['MBR'] = self.memoria.ler(self.registradores['MAR'])

        # Vai pro IR
        self.registradores['IR'] = self.registradores['MBR']

        # PC aponta pro próximo
        self.registradores['PC'] += 1
        

    def decodificacao(self) -> tuple:
        '''Ela vai ler a instrução recebida e vai quebrar ela (fazendo um split) e interpretar'''

        partes = self.registradores['MBR'].split(maxsplit=1) # aqui eu to separando a operação dos operandos, tipo ['ADD'] e ['A, B']
        
        operacao = partes[0]
        operandos = partes[1]
    
        operandos_separados = operandos.split(',') #aqui eu separo os operandos pela virgula, tipo ['A', 'B']

        return operacao, operandos_separados #dá pra retornar uma tupla ou uma lista de lista, o que fizer mais sentido

    def execucao(self, operacao, operandos):
        '''Na teoria seria um monte de if elif elif else pra cada operação que pode receber, tem algum jeito mais bonito de fazer isso?
        LOAD, MUL - multiplica, STOR - armazena na memoria, SUB- subtrai, JUMP - pula '''

        if operacao == 'LOAD':
            if len(operandos) == 1:
                registrador = 'AC'
                endereco = int(operandos[0], 16)
            else: 
                registrador = operandos[0]
                endereco = int(operandos[1],16)
                
            self.registradores[registrador] = self.memoria.ler(endereco)
            print(f'Registrador {registrador} atualizado com o valor {memoria} da memória no endereço {endereco}')
        elif operacao == 'MULT':
            #LOAD MQ, M(0x05)
            #MULT M(0x06)
            #MQ = MQ * M(0x06)

            endereco = int(operandos[0],16)
            memoria = self.memoria.ler(endereco)
            resultado = self.registradores['MQ'] * memoria

            parte_alta = resultado // MAX_VALOR_PALAVRA
            parte_baixa = resultado % MAX_VALOR_PALAVRA

            self.registradores['AC'] = parte_alta
            self.registradores['MQ'] = parte_baixa


            print(f'Resultado da multiplicação: AC = {self.registradores['AC']}, MQ = {self.registradores['MQ']}')

        elif operacao == 'STOR':
            if len(operandos) == 1:
                registrador = 'AC'
                endereco = int(operandos[0], 16)
            else: 
                registrador = operandos[0]
                endereco = int(operandos[1],16)
            
            valor = self.registradores[registrador]
            self.memoria.escrever(endereco, valor)

            print(f'Valor {valor} armazenado no endereço {endereco} da memória')

        elif operacao == 'SUB':
            ''' '''
            if len(operandos) == 1:
                registrador = 'AC'
                endereco = int(operandos[0], 16)
            else: 
                registrador = operandos[0]
                endereco = int(operandos[1],16)
        
            resultado, flag_z, flag_c = self.ula.subtracao(registrador, endereco)
            self.registradores[registrador] = resultado
            self.registradores['Z'] = flag_z
            self.registradores['C'] = flag_c
            print(f'Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')

        elif operacao == 'JUMP':
            # JUMP 0X10

            self.registradores['PC'] = int(operandos[0], 16)            
            print(f'Realizado um JUMP para o endereco {self.registradores['PC']}')            

        elif operacao == 'JUMP+':
            #JUMP+ M(X)
            if registrador['Z'] >= 0:
                self.registradores['PC'] = int(operandos[0], 16)
                print(f'Realizado um JUMP+ para o endereco {self.registradores['PC']}')
                                        
        elif operacao == 'ADD':
            ''''''            
            if len(operandos) == 1:
                registrador = 'AC'
                endereco = int(operandos[0], 16)
            else: 
                registrador = operandos[0]
                endereco = int(operandos[1],16)
        
            resultado, flag_z, flag_c = self.ula.soma(registrador, endereco)
            self.registradores[registrador] = resultado
            self.registradores['Z'] = flag_z
            self.registradores['C'] = flag_c
            print(f'Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')

    def pausa_instrucao(self):
        '''Função que para o ciclo e so volta com o enter'''
        while True:
            pausa = input('Digite enter para realizar 2 operações...')
            instrucao = self.memoria.ler(self.registradores['PC'])

            if instrucao == None or instrucao == 0:
                break
            
            for i in range(2):
                self.busca()
                operacao, operandos_separados = self.decodificacao()
                self.execucao(operacao, operandos_separados)
            print("Final das 2 primeiras operaçoes")

class ULA:

    def soma(self, valor1, valor2):
        resultado_inicial = valor1 + valor2
        
        if resultado_inicial >= MAX_VALOR_PALAVRA:
            flag_c = 1
        else:
            flag_c = 2
        
        resultado_final = resultado_inicial % MAX_VALOR_PALAVRA
        
        if resultado_final == 0:
            flag_z = 0
        else:
            flag_z = 1
        
        return resultado_final, flag_z, flag_c

    def subtract(self, valor1, valor2):
        resultado = valor1 - valor2
        
        if resultado < 0:
            flag_z = -1
            flag_c = 1
        elif resultado == 0:
            flag_z = 0
            flag_c = 2
        else:
            flag_z = 1
            flag_c = 2
            
        return resultado, flag_z, flag_c
            
            
def inicializa():
    if os.path.exists('teste.txt'):
        with open('teste.txt', 'r') as arq_operacoes:
            lista_operacoes_memoria = arq_operacoes.readlines()
            op_memoria = True
            memoria: list = []
            operacoes: list = []
            for op in lista_operacoes_memoria:
                if op == '\n':
                    op_memoria = False
                elif op_memoria:
                    memoria.append(op.strip('\n'))
                else:
                    operacoes.append(op.strip('\n'))             
        print(f'Memorias: {memoria}\nOperacoes: {operacoes}') 
    #else:
    print("Erro")

      
def main():
      inicializa()


if __name__ == "__main__":
    main()