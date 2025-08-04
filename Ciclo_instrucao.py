# Alunos: 
# Isadora Dantas Bruchmam (ra140870)
# João Vitor Bidoia Ângelo(ra139617)
# Letícia Akemi Nakahati Vieira (ra140535)

from __future__ import annotations
import os

TAMANHO_PALAVRA_BITS = 40
MAX_VALOR_PALAVRA = 2 ** TAMANHO_PALAVRA_BITS 

class Memoria:
    '''
    Simula a memória principal do computador
    Ela é implementada como uma lista(vetor) em que cada índice representa um endereço de memória. Sua responsabilidade se relaciona
    com o armazenamento e recuperação de dados e instruções
    '''
    def __init__(self, tamanho):
        '''
        Inicializa a memória

        parâmetros:
        tamanho = O número total de palavras que a memória armazena
        memoria = lista inicializada com o tamanho da memória
        '''
        self.tamanho = tamanho
        self.memoria = [0] * tamanho

    def escrever (self, endereco, dado):
        '''
        Função que recebe um endereço e um dado, e armazena/escreve esse dado no endereço recebido

        parâmetros:
        endereco = O índice da lista que o dado será armazenado 
        dado = O valor que será armazenado, pode ser um inteiro ou uma string
        '''
        self.memoria[endereco] = dado
    
    def ler (self, endereco):
        '''
        Função que recebe um endereço e retorna o dado armazenado na posição

        parâmetros:
        endereco = O índice da lista de onde o dado será lido

        o retorno é o dado que está armazenado na memória

        '''
        return self.memoria[endereco]

class CPU:
    '''
    A unidade central de processamento (CPU) é o "cérebro" das operações

    Essa classe possui a responsabilidade da coordenação de do gerenciamento do programa através do PC e utiliza os componentes
    Memoria e ULA para buscar, decodificar e executar as instruções
    '''
    def __init__(self, memoria, ula):
        '''
        Inicializa a CPU, conectando a mesma com a memória e a ULA
        
        Define também o conjunto dos registradores que serão utilizados na simulação, sendo eles
        PC - contador; MAR - endereço de memória; MBR - buffer de memória; IR - instrução; AC - acumulador;
        C - flag de carry out (1 houve carry, 2 não houve carry); Z - flag de resultado zero ( -1 resultado negativo,
        0 resultado 0, 1 resultado positivo); MQ - multiplicador; R - resto da divisão
        '''
        self.ula = ula
        self.memoria = memoria
        self.arquivo_operacao = inicializa() #open("readme.txt", 'r')
        self.registradores = {
            'PC': 0, 'MAR': 0, 'MBR': None, 'IR': None, 'IBR': None,
            'AC': 0, 'C': 0, 'Z': 0, 'MQ': 1, 'R': 0, 'A': 0, 'B': 0, 'C1': 0, 'D': 0
        }

    def busca(self):
        '''
        Essa função simula a busca de um ciclo de instrução
        MAR <- PC = O endereço da próxima instrução é colocado no MAR
        MBR <- (memória[MAR]) = O conteúdo da memória no endereço é lido para o MBR
        PC <- PC + 1 = O PC aponta para a próxima instrução em sequência
        IR <- MBR = A instrução é movida para o IR para ser decodificada
        '''
        self.registradores['MAR'] = self.registradores['PC']
        self.registradores['MBR'] = self.memoria.ler(self.registradores['MAR'])
        self.registradores['PC'] += 1
        self.registradores['IR'] = self.registradores['MBR']

    def decodificacao(self) -> tuple:
        '''
        Essa função simula a decodificação de um ciclo de instrução
        Analisa a string presente no IR , separando a mesma em operação(como ['LOAD']) e operandos (como ['AC', '0X10']

        Retorna uma tupla com essas duas listas separadas
        '''
        instrucao = self.registradores['IR']
        if not isinstance(instrucao, str):
            return 'NOP', []

        partes = self.registradores['IR'].split(maxsplit=1) 
    
        operacao = partes[0]
        operandos = partes[1]
        if len(operandos) > 1:
            operandos = operandos.split(',')
        for i in range(len(operandos)):
            operandos[i].replace(' ', '') 
                  
        return operacao, operandos

    def execucao(self, operacao, operandos):
        '''
        Essa função simula a execução de um ciclo de instrução.
        
        Parâmetros:
        operacao = String com o comando (como LOAD)
        operandos = Uma lista com os parâmetros da operação (como MQ, M(0x101))

        A partir dos parâmetros recebidos, chama a função que realiza a operação correspondente, 
        seja uma transferência de dados, uma operação aritmética, lógica ou um desvio de fluxo

        A CPU realiza uma série de operações, e as executadas nessa simulação são:
        LOAD - carrega um valor da memória para um registrador (o padrão, caso não haja é o AC)
        MUL - multiplica MQ por um valor na memória, salvando o resultado em AC e MQ
        STOR - armazena o valor de um registrador na memória (o padrão, caso não haja é o AC)
        SUB- subtrai um valor da memória de um registrador (o padrão, caso não haja é o AC) e atualiza as flags Z e C 
        JUMP - desvia o fluxo do programa para outro endereço de memória
        JUMP+ - desvia o fluxo somente se o resultado da última operação foi positivo ou zero
        ADD - soma um valor da memória a um registrador (o padrão, caso não haja é o AC) e atualiza as flags Z e C
        MOV - copia o valor de um registrador para outro registrador
        DIV - divide o AC por um valor da memória, guardando o quociente no MQ e o resto em AC
        RSH - desloca todos os bits do AC uma posição para a esquerda (como se multiplicasse por 2)
        LSH - desloca todos os bits do AC uma posição para a direita (como se dividisse por 2)
        '''

        if operacao == 'LOAD':
            self.executa_load(operandos)
        elif operacao == 'MUL':
            self.executa_mul(operandos)
        elif operacao == 'STOR':
            self.executa_stor(operandos)
        elif operacao == 'SUB':
            self.executa_sub(operandos)
        elif operacao == 'JUMP':
           self.executa_jump(operandos)
        elif operacao == 'JUMP+':
            self.executa_jumpmais(operandos)     
        elif operacao == 'ADD':         
          self.executa_add(operandos)
        elif operacao == 'MOV':
            self.executa_mov(operandos)
        elif operacao == 'DIV':
            self.executa_div(operandos)
        elif operacao == 'RSH':
            self.executa_rsh(operandos)
        elif operacao == 'LSH':
            self.executa_lsh(operandos)
        else:
            print('Operação inexistente, verifique o arquivo')
            
    def executa_mul(self, operandos):
        #LOAD MQ, M(0x05)
        #MULT M(0x06)
        #MQ = MQ * M(0x06)

        endereco = int(operandos[0].replace('M(', '').replace(')', ''),16)
        memoria = self.memoria.ler(endereco)
        resultado = int(self.registradores['MQ']) * memoria
        print(resultado)

        parte_alta = resultado // MAX_VALOR_PALAVRA
        parte_baixa = resultado % MAX_VALOR_PALAVRA

        self.registradores['AC'] = parte_alta
        self.registradores['MQ'] = parte_baixa

        print(f'Resultado da multiplicação: AC = {self.registradores['AC']}, MQ = {self.registradores['MQ']}')       
            
            
    def executa_mov(self, operandos):
        # fonte: registrador/valor imediato | destino: registrador MOV MQ
        #MOV A, MQ .... A <- MQ
            if len(operandos) == 1:
                reg_origem = operandos[0]            
                if reg_origem in self.registradores: # MOV MQ
                    self.registradores['AC'] = self.registradores[reg_origem] #MQ
                    print(f'MOV em modo endereçamento por registrador, leitura do dado {self.registradores['AC']}')                   
            elif len(operandos) == 2: #MOV A, B 
                reg_destino = operandos[0].replace(' ','')
                reg_origem = operandos[1].replace(' ','')
                print(reg_destino, reg_origem)
                if reg_destino in self.registradores and reg_origem in self.registradores:
                    self.registradores[reg_destino] = self.registradores[reg_origem]
                    print(f'MOV em modo endereçamento imediato, {reg_destino} ← {reg_origem} ({self.registradores[reg_origem]})')

                else: 
                    print('n foii')
                
    def executa_stor(self, operandos):
        if len(operandos) == 1:
            registrador = 'AC'
            endereco = int(operandos[0].replace('M(', '').replace(')', ''), 16)
        else: # STOR M(10x10), A
            print(operandos)
            endereco = int(operandos[0].replace('M(', '').replace(')', ''),16)
            registrador = operandos[1].replace(' ', '')
            print('r',registrador)
            print('e',endereco)
        
        valor = self.registradores[registrador]
        self.memoria.escrever(endereco, valor)

        print(f'STOR: Valor {valor} armazenado no endereço {endereco} da memória')
            
    def executa_jump(self, operandos):
        # JUMP M(0X10)
        self.registradores['PC'] = int(operandos[0].replace('M(', '').replace(')', ''), 16)            
        print(f'Realizado um JUMP para o endereco {self.registradores['PC']}')  

    def executa_jumpmais(self, operandos):
        if self.registradores['Z'] >= 0:
            self.registradores['PC'] = int(operandos[0].replace('M(', '').replace(')', ''), 16) 
            print(f'Realizado um JUMP+ para o endereco {self.registradores['PC']}')
        else:
            print(f"JUMP+: Condição Z>=0 NÃO atendida. Salto ignorado.")
               

    def executa_load(self, operandos):
            if len(operandos) == 1:
               registrador = 'AC'
               operando_origem = operandos[0]
            else:
               registrador = operandos[0]
               operando_origem = operandos[1]

            endereco = int(operando_origem.replace('M(', '').replace(')', ''),16)
            dado = self.memoria.ler(endereco)
            print(f'LOAD realizado, leitura do dado {dado} do endereco {endereco}')
        
            self.registradores[registrador] = dado
                
    def executa_add(self, operandos):
        if len(operandos) == 1:
            registrador = 'AC'
            operando_origem = operandos[0].replace(' ', '')
        else: 
            registrador = operandos[0]
            operando_origem = operandos[1].replace(' ', '')
        #ADD A, M(0x101)
        if operando_origem.startswith('M('): #Endereçamento direto
            endereco = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
            valor2 = self.memoria.ler(endereco)
        else: #Endereçamento imediato, ADD A
            valor2 = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
        
        self.registradores[registrador], self.registradores['Z'], self.registradores['C'] = self.ula.soma(valor1, valor2)
        print(f'Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')
                        
    def executa_sub(self, operandos):
        if len(operandos) == 1:
            registrador = 'AC'
            operando_origem = operandos[0].replace(' ', '')
        else: 
            registrador = operandos[0]
            operando_origem = operandos[1].replace(' ','')
            
        if operando_origem.startswith('M('):
            endereco = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
            valor2 = self.memoria.ler(endereco)
        else:
            valor1 = int(self.registradores[registrador])
            valor2 = int(operando_origem.replace('M(', '').replace(')', ''), 16)
        self.registradores[registrador], self.registradores['Z'], self.registradores['C'] = self.ula.subtracao(valor1, valor2)
        print(f'Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')
    
    def pausa_instrucao(self):
        '''
        Função que inicia e controla o ciclo da instrução principal, pausando a cada duas operações,
        sendo necessário clicar em enter para continuar
        '''
        print('--------------------------------')
        print('Estado inicial dos registradores')
        self.mostra_registradores()
        simulacao = True
        while simulacao:
            input('\nDigite enter para realizar 2 operações...\n')
           
            for _ in range(2):
                instrucao = self.memoria.ler(self.registradores['PC'])

                if instrucao == None or instrucao == 0:
                    simulacao = False
                else:
                    self.busca()
                    operacao, operandos_separados = self.decodificacao()
                    self.execucao(operacao, operandos_separados)
                    print('--------------------------------')
                    print('Estado dos registradores:')
                    self.mostra_registradores()
                    
        if simulacao:
            print("Final das 2 primeiras operaçoes")
        print('Fim!!')

    def mostra_registradores(self):
        '''
        Para cada instrução, printa os registradores utilizados
        '''
        print(f'PC - {self.registradores['PC']}')
        print(f'AC - {self.registradores['AC']}')
        print(f'MAR - {self.registradores['MAR']}')
        print(f'MBR - {self.registradores['MBR']}')
        print(f'IR - {self.registradores['IR']}')
        print(f'MQ - {self.registradores['MQ']}')
        print(f'Z - {self.registradores['Z']}')
        print(f'C - {self.registradores['C']}')
        print(f'R - {self.registradores['R']}')
        print(f"A - {self.registradores['A']}")
        print(f"B - {self.registradores['B']}") if self.registradores['B'] else ''
        print(f"C1 - {self.registradores['C1']}") if self.registradores['C1'] else ''
        print(f"D - {self.registradores['D']}") if self.registradores['D'] else ''
        print('--------------------------------')
        
class ULA:
    '''
    Representa a unidade lógica e aritmética (ULA) do simulador, responsável pela realização das operações de cálculo
    Funciona como uma "calculadora" para a CPU: recebe os valores, executa a operação e retorna o resultado com as flags
    Z e C

    A ULA é um componente que não armazena nenhum valor permanente, tendo em vista que o controle é feito pela CPU
    '''
    def __init__(self):
        '''
        Como é um componente que não armazena valores, não tem elementos a serem inicializados
        '''

    def soma(self, valor1, valor2):
        '''
        Função que realiza a soma de dois valores 
        Calcula o resultado da adição e determina o status dos registradores Z e C. o Carry é ativado se houver overflow da
        capacidade de 40 bits (computador IAS)

        parâmetros:
        valor1 = Primeiro número da adição (normalmente um registrador)
        valor2 = Segundo número da adição (normalmente da memória)

        ela retorna o resultado da operação(resultado_final), e as duas flags (flag_z e flag_c)
        '''
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

    def subtracao(self, valor1, valor2):
        '''
        Função que realiza a subtração de dois valores 
        Calcula o resultado e determina o status dos registradores Z e C
        Na subtração, o carry atua como "borrow flag"

        parâmetros:
        valor1 = Primeiro número da subtração (normalmente um registrador)
        valor2 = Segundo número da subtração (normalmente da memória)

        ela retorna o resultado da operação, e as duas flags (flag_z e flag_c)
        '''
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
    '''
    Função responsável pela abertura do arquivo e retorno de duas listas: 
    '''
    if os.path.exists('selecao.txt'):
        with open('selecao.txt', 'r') as arq_operacoes:
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
        return memoria, operacoes
    #else:
    print("Erro")

      
def main():
    memoria_principal = Memoria(4096) #tem q ver o tamanho dela
    ula = ULA()
    processador = CPU(memoria_principal, ula)

    memoria, operacoes = inicializa()

    for i in memoria:
        partes = i.split()
        if len(partes) == 2:
            valor_int = int(partes[0])
            endereco_int = int(partes[1], 16)
            memoria_principal.escrever(endereco_int, valor_int)
    
    endereco_inicio = 0x0A
    endereco_atual = endereco_inicio

    for instrucao in operacoes:
        memoria_principal.escrever(endereco_atual, instrucao)
        endereco_atual +=1
    
    processador.registradores['PC'] = endereco_inicio
    processador.pausa_instrucao()
    print(memoria_principal.memoria)

if __name__ == "__main__":
    main()