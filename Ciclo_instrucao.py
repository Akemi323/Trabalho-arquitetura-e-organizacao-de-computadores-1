# Alunos: 
# Isadora Dantas Bruchmam (ra140870)
# João Vitor Bidoia Ângelo(ra139617)
# Letícia Akemi Nakahati Vieira (ra140535)
from __future__ import annotations
import os
import sys

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
        self.registradores = {
            'PC': None, 'MAR': 0, 'MBR': None, 'IR': None, 'IBR': None,
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
        partes = self.registradores['IR'].split(maxsplit=1)

        if len(partes) > 1:
            operacao = partes[0] 
            operandos = partes[1]
            if len(operandos) > 1:
                operandos = operandos.split(',')
                for i in range(len(operandos)):
                    operandos[i] = operandos[i].replace(' ', '')
                return operacao, operandos
            else:  
                return operacao, [operandos]
        else:
            operacao = partes[0]
            return operacao, []

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

    def executa_load(self, operandos):
        '''
        Função que executa a instrução de carregamento (LOAD)

        tipos de instruções que aceita:
        1. LOAD A, M(0x103) 
        2. LOAD M(0x103)
        3. LOAD M(A)
        4. LOAD A, M(B)

        Parâmetros:
        operandos = Lista com os operandos
        '''
        if len(operandos) == 1: # LOAD M(A); LOAD M(0x100)
            registrador = 'AC'
            operando_origem = operandos[0]
        else: # LOAD A, M(B); LOAD A, M(0x100)
            registrador = operandos[0]
            operando_origem = operandos[1]
          
        operando_origem = operando_origem.replace('M(', '').replace(')', '')
        
        if operando_origem in self.registradores: # LOAD M(A); LOAD A, M(A)
            endereco = self.registradores[int(self.registradores[operando_origem],16)]
        else: # LOAD M(0X103); LOAD A, M(0x103)
            endereco = int(operando_origem, 16)
        
        dado = self.memoria.ler(endereco)
        print(f'LOAD: leitura do dado {dado} do endereco {endereco}')
    
        self.registradores[registrador] = dado
                
            
    def executa_mul(self, operandos):
        '''
        Função que executa a instrução de multiplicação (MUL)

        tipos de instruções que aceita:
        1. MUL M(0x06)

        Parâmetros:
        operandos = Lista com os operandos
        '''

        endereco = int(operandos[0].replace('M(', '').replace(')', '') , 16)
    
        valor1 = self.memoria.ler(endereco)
        valor2 = self.registradores['MQ']

        parte_alta, parte_baixa, flag_z, flag_c = self.ula.multiplicacao(valor1, valor2)

        self.registradores['AC'] = parte_alta
        self.registradores['MQ'] = parte_baixa
        self.registradores['Z'] = flag_z
        self.registradores['C'] = flag_c
        

        print(f'MUL: Resultado da multiplicação: AC = {parte_alta}, MQ = {parte_baixa}, Z = {flag_z}, C = {flag_c}')
                
    def executa_stor(self, operandos):
        '''
        Função que executa a instrução de armazenamento na memória (STOR)

        tipos de instruções que aceita:
        1. STOR M(0x102), A
        2. STOR M(0X03)
        3. STOR M(A)
        4. STOR M(A), B

        Parâmetros:
        operandos = Lista com os operandos
        '''
        if len(operandos) == 1: # STOR M(A); STOR M(0x20)
            registrador = 'AC'
            endereco = operandos[0]
        else: # STOR M(10x10), A; STOR M(A), B
            endereco = operandos[0]
            registrador = operandos[1].replace('M(', '').replace(')', '')
        
        endereco = endereco.replace('M(', '').replace(')', '')
        
        if endereco in self.registradores: # STOR M(A); STOR M(A), B
            endereco = int(self.registradores[endereco],16)
        else: # STOR M(0x102); STOR M(0x102), A
            endereco = int(endereco, 16)
                
        valor = self.registradores[registrador]
        self.memoria.escrever(endereco, valor)

        print(f'STOR: Valor {valor} armazenado no endereço {endereco} da memória')

    def executa_sub(self, operandos):
        '''
        Função responsável pela execução da instrução de subtração (SUB).

        Funciona de forma idêntica ao ADD, mas realiza uma subtração.
        Lida com endereçamento Direto e Imediato.

        tipos de instruções que aceita:
        1. SUB M(0x101) - endereçamento direto
        2. SUB 0x101 - endereçamento imediato
        3. SUB A, M(0x101) - endereçamento direto
        4. SUB A, 0x101 - endereçamento imediato
        5. SUB B

        Parâmetros:
        operandos = Lista com os operandos
        '''
        if len(operandos) == 1: # SUB M(0x101); SUB 0x101
            registrador = 'AC'
            operando_origem = operandos[0]
        else: # SUB A, M(0x101); SUB A, 0x101
            registrador = operandos[0]
            operando_origem = operandos[1]
            
        if operando_origem.startswith('M('): #endereçamento direto
            endereco = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
            valor2 = self.memoria.ler(endereco)
        else: # endereçamento imediato
            operando_origem = operando_origem.replace('M(', '').replace(')', '')
            valor1 = int(self.registradores[registrador])
            if operando_origem in self.registradores:
                valor2 = int(self.registradores[operando_origem])
            else:
                valor2 = int(operando_origem, 16)
            print(valor1, valor2)
        self.registradores[registrador], self.registradores['Z'], self.registradores['C'] = self.ula.subtracao(valor1, valor2)
        print(f'SUB: Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')
            
    def executa_jump(self, operandos):
        '''
        Função que executa a instrução de desvio (JUMP)

        tipos de instruções que aceita:
        1. JUMP M(0x03)
        2. JUMP 0x03

        Parâmetros:
        operandos = Lista com os operandos
        '''
        self.registradores['PC'] = int(operandos[0].replace('M(', '').replace(')', ''), 16)            
        print(f'JUMP: Realizado um desvio para o endereco {self.registradores['PC']}')  

    def executa_jumpmais(self, operandos):
        '''
        Função que executa a instrução de desvio com a condicional de não negativo (JUMP+)

        tipos de instruções que aceita:
        1. JUMP+ M(0x03)
        2. JUMP+ 0x03

        Parâmetros:
        operandos = Lista com os operandos
        '''
        if self.registradores['Z'] >= 0:
            self.registradores['PC'] = int(operandos[0].replace('M(', '').replace(')', ''), 16) 
            print(f'JUMP+: Realizado um desvio para o endereco {self.registradores['PC']}')
        else:
            print(f"JUMP+: Condição Z>=0 NÃO atendida. Salto ignorado.")
               
    def executa_add(self, operandos):
        '''
        Função responsável pela execução da instrução de adição (ADD).

        Lida com endereçamento Direto (M(X)) e Imediato (um número) para
        somar um valor a um registrador (padrão AC) e atualizar os flags.

        Tipos de instruções que aceita:
        1. ADD M(0x101) - endereçamento direto
        2. ADD A, 0x101 - endereçamento imediato
        3. ADD 0x101 - endereçamento imediato
        4. ADD A, M(0x101) - endereçamento direto

        Parâmetros:
        operandos - Lista com os operandos
        '''
        if len(operandos) == 1: # ADD M(0x101); ADD 0x101
            registrador = 'AC'
            operando_origem = operandos[0]
        else: # ADD A, 0x101, ADD A, M(0x101)
            registrador = operandos[0]
            operando_origem = operandos[1]
        if operando_origem.startswith('M('): #Endereçamento direto
            endereco = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
            valor2 = self.memoria.ler(endereco)
        else: #Endereçamento imediato, ADD A
            valor2 = int(operando_origem.replace('M(', '').replace(')', ''),16)
            valor1 = int(self.registradores[registrador])
        
        self.registradores[registrador], self.registradores['Z'], self.registradores['C'] = self.ula.soma(valor1, valor2)
        print(f'SUB: Resultado da subtração: {registrador}, Z = {self.registradores['Z']}, C = {self.registradores['C']}')

    def executa_mov(self, operandos):
        '''
        Função que executa a instrução de movimentação de dados entre os registradores (MOV)

        tipos de instruções que aceita:
        1. MOV A
        2. MOV A, B
        3. MOV 0x20
        4. MOV A, 0x20

        Parâmetros:
        operandos = Lista com os operandos
        '''
        if len(operandos) == 1: # MOV A, MOV 0X20
            reg_origem = operandos[0]            
            if reg_origem in self.registradores: 
                self.registradores['AC'] = self.registradores[reg_origem] 
                print(f'MOV: modo endereçamento por registrador, leitura do dado {self.registradores['AC']}')                   
        elif len(operandos) == 2: #MOV A, 0X20, MOV A, B
            reg_destino = operandos[0]
            reg_origem = operandos[1]
            if reg_destino in self.registradores and reg_origem in self.registradores:
                self.registradores[reg_destino] = self.registradores[reg_origem]
                print(f'MOV: modo endereçamento imediato, {reg_destino} ← {reg_origem} ({self.registradores[reg_origem]})')
            else:
                self.registradores[reg_destino] = reg_origem
                print(f'MOV: modo endereçamento imediato, {reg_destino} ← {reg_origem}')

    
    def executa_div(self, operandos):
        '''
        Função que executa a instrução de divisão (DIV)

        tipos de instruções que aceita:
        1. DIV M(0x03)

        Parâmetros:
        operandos = Lista com os operandos
        '''
        endereco = int(operandos[0].replace('M(', '').replace(')', ''),16)

        valor1 = self.registradores['AC']
        valor2 = self.memoria.ler(endereco)

        resultado, resto, flag_z, flag_c = self.ula.divisao(valor1, valor2)
        self.registradores['MQ'] = resultado
        self.registradores['R'] = resto
        self.registradores['Z'] = flag_z
        self.registradores['C'] = flag_c
        
        print(f'DIV: Resultado da divisao: {resultado}, Resto = {resto}, Z = {flag_z}, C = {flag_c}')


    def executa_rsh(self):
        '''
        Função que executa o deslocamento de todos os bits do AC para a esquerda (RSH)

        tipos de instruções que aceita:
        1. RSH

        Parâmetros:
        operandos = Lista com os operandos
        '''
        valor = self.registradores['AC']
        resultado, flag_c = self.ula.pos_esquerda(valor)

        resultado = self.registradores['AC']
        flag_c = self.registradores['C']

        print(f'RSH: bits deslocado para a esquerda: Resultado = {resultado}, C = {flag_c}')




    def executa_lsh(self):
        '''
        Função que executa o deslocamento de todos os bits do AC para a direita (LSH)

        tipos de instruções que aceita:
        1. LSH

        Parâmetros:
        operandos = Lista com os operandos
        '''
        valor = self.registradores['AC']
        resultado, flag_c = self.ula.pos_direita(valor)

        resultado = self.registradores['AC']
        flag_c = self.registradores['C']

        print(f'RSH: bits deslocado para a direita: Resultado = {resultado}, C = {flag_c}')


    def pausa_instrucao(self):
        '''
        Função que inicia e controla o ciclo da instrução principal, pausando a cada duas operações,
        sendo necessário clicar em enter para continuar
        '''
        print('-----------------------------------------------------')
        print('Estado inicial dos registradores')
        self.mostra_registradores()
        simulacao = True
        while simulacao:
            print('-----------------------------------------------------')
            input('\nDigite enter para realizar 2 instruções...\n')
           
            for _ in range(2):
                instrucao = self.memoria.ler(self.registradores['PC'])
                if instrucao == None or instrucao == 0:
                    simulacao = False
                else:
                    self.busca()
                    operacao, operandos_separados = self.decodificacao()
                                        
                    print('-----------------------------------------------------')
                    self.execucao(operacao, operandos_separados)
                    print('-----------------------------------------------------')
                    print('Estado dos registradores:')
                    self.mostra_registradores()

        print('-----------------------------------------------------')        
        print('Fim das instruções!')

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
        print(f"B - {self.registradores['B']}")
        print(f"C1 - {self.registradores['C1']}")
        print(f"D - {self.registradores['D']}")
        
class ULA:
    '''
    Representa a unidade lógica e aritmética (ULA) do simulador, responsável pela realização das operações de cálculo
    Funciona como uma "calculadora" para a CPU: recebe os valores, executa a operação e retorna o resultado com as registradores
    Z, C e R

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
    
    def divisao(self, valor1, valor2):
        '''
        Função que realiza a divisão de dois valores
        Calcula o resultado e determina o status dos registradores Z e C

        Parâmetros:
        valor 1 = dividendo
        valor 2 = divisor

        Se a divisão for por 0, retorna um de erro
        Se não, retorna o resultado, o resto e as duas flags( flag_z e flag_c)
        '''
        if valor2 != 0:
            resultado = valor1 // valor2
            resto = valor1 % valor2
            flag_c = 2
            if resultado == 0:
                flag_z = 0
            else:
                flag_z = 1
            return resultado, resto, flag_z, flag_c
        else:
            print("ERRO: divisão por zero")
            flag_c = 1
            flag_z = -1
            return 0,0,flag_z, flag_c


    def multiplicacao(self, valor1, valor2):
        '''
        Função que realiza a multiplicacão de dois valores
        Calcula o resultado e determina o status dos registradores Z e C

        Parâmetros:
        valor 1 = primeiro número da multiplicação (um endereço)
        valor 2 = segundo número da multiplicação (o MQ)

        Se a divisão for por 0, retorna um de erro
        Se não, retorna o resultado, o resto e as duas flags( flag_z e flag_c)
        '''
        resultado = valor1 * valor2

        parte_alta = resultado // MAX_VALOR_PALAVRA
        parte_baixa = resultado % MAX_VALOR_PALAVRA

        if resultado == 0:
            flag_z = 0
        else: 
            flag_z = 1

        if parte_alta != 0:
            flag_c = 1
        else:
            flag_c = 2
    
        return parte_alta, parte_baixa, flag_z, flag_c

    def pos_esquerda(self, valor):
        '''
        Função que realiza o deslocamento de todos os bits um valor para a esquerda
        na prática, multiplica por 2

        Parâmetros:
        valor = número que será deslocado

        retorna o resultado e a flag_c
        '''
        resultado = valor * 2

        if resultado > TAMANHO_PALAVRA_BITS:
            flag_c = 1
        else:
            flag_c = 2
        
        resultado_final = resultado % MAX_VALOR_PALAVRA
        return resultado_final, flag_c
    
    def pos_direita(self, valor):
        '''
        Função que realiza o deslocamento de todos os bits um valor para a direita
        na prática, divide por 2

        Parâmetros:
        valor = número que será deslocado

        retorna o 
        '''
        resultado = valor % 2

        if resultado > TAMANHO_PALAVRA_BITS:
            flag_c = 1
        else:
            flag_c = 2

        resultado_final = valor // 2
        return resultado_final, flag_c
        
            
def inicializa(nome_arq):
    '''
    Função responsável pela abertura do arquivo e retorno de duas listas: 
    '''
    if os.path.exists(nome_arq):
        with open(nome_arq, 'r') as arq_operacoes:
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
    if len(sys.argv) != 3:
        print("Uso: python Ciclo_instrucao.py <-f ou -s> <endereço da primeira instrução>")
        sys.exit(1)

    flag = sys.argv[1]
    endereco = sys.argv[2]
    if flag == '-f':
        nome_arq = 'fatorial.txt'
    elif flag == '-s':
        nome_arq = 'selecao.txt'
    else:
        print('Flag inválida. Use -f para executar o algoritmo fatorial ou -s para executar o Selection Sort')
        sys.exit(1)

    try:
        endereco_inicio = int(endereco, 16)
    except ValueError:
        print("Erro: endereço deve estar em hexadecimal. Ex: 0x0A")
        sys.exit(1)    
    
    memoria_principal = Memoria(4096)
    ula = ULA()
    processador = CPU(memoria_principal, ula)

    memoria, operacoes = inicializa(nome_arq) 

    for i in memoria:
        partes = i.split()
        if len(partes) == 2:
            valor_int = int(partes[0])
            endereco_int = int(partes[1], 16)
            memoria_principal.escrever(endereco_int, valor_int)

    endereco_atual = endereco_inicio

    for instrucao in operacoes:
        memoria_principal.escrever(endereco_atual, instrucao)
        endereco_atual +=1
    
    processador.registradores['PC'] = endereco_inicio
    processador.pausa_instrucao()

    if 'fatorial' in nome_arq:
        resultado = memoria_principal.ler(0x1FF) 
        print(f"O resultado do Fatorial foi: {resultado}")
        print('-----------------------------------------------------')

    if 'selecao' in nome_arq:
        print(f"O resultado da Seleção ")
        print(memoria_principal.ler(0x100))
        print(memoria_principal.ler(0x101))
        print(memoria_principal.ler(0x102))
        print(memoria_principal.ler(0x103))
        print('-----------------------------------------------------')
            

if __name__ == "__main__":
    main()