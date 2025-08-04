Projeto: Simulador de CPU Baseada em IAS

Disciplina: ARQUITETURA E ORGANIZAÇÃO DE COMPUTADORES
Curso: Bacharelado em Ciência da Computação
Data de Entrega: 04/08/2025 
Professor: Rodrigo Calvo 

## 1. Autores

- Isadora Dantas Bruchmam, RA: 140870
- João Vitor Bidoia Ângelo, RA: 139617
- Letícia Akemi Nakahati Vieira, RA: 140535


## 2. Descrição do Projeto
Este projeto implementa um simulador em Python para uma arquitetura de computador inspirada no modelo IAS. O objetivo é simular o ciclo de instrução de um processador, permitindo a execução de programas em uma linguagem de máquina simplificada e a visualização do estado dos registradores a cada passo. O simulador foi construído de forma modular, com classes que representam a CPU, a Memória e a ULA.

## 3. Funcionalidades e Instruções Implementadas
- Simulação completa do ciclo de Busca, Decodificação e Execução.
- Memória de 4096 palavras, com cada palavra tendo um tamanho conceitual de 40 bits.
- CPU com registradores principais (PC, MAR, MBR, IR, AC, MQ) e de status (Z, C).
- ULA sem estado, responsável pelos cálculos aritméticos e lógicos.
- Suporte para Endereçamento Direto e Imediato.
- Conjunto de instruções implementado:
  - **LOAD**: Carrega um dado da memória, de outro registrador ou um valor imediato.
  - **STOR**: Armazena um dado de um registrador na memória.
  - **ADD / ADDI**: Soma um valor da memória ou um valor imediato ao acumulador.
  - **SUB / SUBI**: Subtrai um valor da memória ou um valor imediato do acumulador.
  - **MULT**: Multiplica o valor em MQ por um valor da memória, armazenando o resultado em AC:MQ.
  - **DIV**: Divide o valor em AC por um valor da memória, armazenando o quociente em MQ e o resto em AC.
  - **JUMP**: Desvio incondicional de fluxo.
  - **JUMP+ / JUMP_ZERO / JUMP_NEG**: Desvios condicionais baseados nos flags de status.
  - **MOV**: Copia dados entre registradores.
  - **LSH / RSH**: Deslocamento de bits à esquerda e à direita.

## 4. Como Executar o Simulador

### 4.1. Pré-requisitos
- Python 3.x instalado.

### 4.2. Passos para Execução 
1.  Garanta que o script principal (ex: `Ciclo_instrucao.py`) e o arquivo com o programa de máquina (ex: `teste.txt`) estejam na mesma pasta.

2.  Abra um terminal (Prompt de Comando, PowerShell, etc.) e navegue até a pasta do projeto.

3.  Execute o script com o seguinte comando:
    Para o fatorial:
    python Ciclo_instrucao.py -f <posicao_hexa>
    Para a seleção:
    python Ciclo_instrucao.py -s <posicao_hexa>
    

5.  O simulador irá iniciar, carregar o programa do arquivo na memória e começar a execução. Siga as instruções no terminal (pressionando <ENTER>) para avançar ciclo por ciclo.

## 5. Formato do Arquivo de Entrada (`teste.txt`)
O arquivo de programa (`.txt`) deve seguir o formato que a função `inicializa` do código espera:

1.  **Seção de Dados:** As primeiras linhas contêm os dados para inicializar a memória. Cada linha deve estar no formato:
    <valor_decimal> <endereco_hexadecimal>
    Exemplo: `25 0x100`

2.  **Linha em Branco:** Uma única linha em branco deve separar a seção de dados da seção de instruções.

3.  **Seção de Instruções:** As linhas restantes são as instruções do programa. Elas serão carregadas sequencialmente a partir de um endereço padrão no código.
    Exemplo: `LOAD AC, M(0x100)`

