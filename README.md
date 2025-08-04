# Projeto: Simulador de ciclo de instrução Baseada em IAS

- Disciplina: arquitetura e organização de computadores
- Curso: Bacharelado em Ciência da Computação
- Data de Entrega: 04/08/2025 
- Professor: Rodrigo Calvo 

## 1. Autores

- Isadora Dantas Bruchmam, RA: 140870
- João Vitor Bidoia Ângelo, RA: 139617
- Letícia Akemi Nakahati Vieira, RA: 140535


## 2. Descrição do Projeto
Este projeto consiste em um simulador em Python para uma arquitetura de computador hipotética, fortemente inspirada no modelo IAS de John von Neumann. O simulador implementa os principais componentes de um computador – CPU, ULA e Memória – de forma modular e orientada a objetos.

O objetivo principal é carregar programas escritos em uma linguagem de máquina customizada a partir de arquivos de texto e executar o ciclo de instrução (Busca, Decodificação e Execução) para cada comando, permitindo a observação detalhada do estado dos registradores a cada passo. A simulação pode ser controlada interativamente pelo usuário, que avança a execução pressionando a tecla <ENTER>.

## 3. Arquitetura do Simulador
O simulador foi dividido em três classes principais, representando os componentes lógicos de um computador:

* **`Memoria`**: Simula a memória RAM como um vetor de 4096 palavras. É responsável por `ler()` e `escrever()` dados e instruções em endereços específicos.

* **`ULA` (Unidade Lógica e Aritmética)**: Atua como a "calculadora" do processador. É uma classe sem estado que recebe valores numéricos, realiza operações (soma, subtração, multiplicação, etc.) e retorna o resultado e o estado atualizado dos flags de status (`Z` e `C`) para a CPU.

* **`CPU`**: É o componente central e o "cérebro" do simulador. Contém o dicionário de registradores, orquestra o ciclo de instrução através do método `run()` (no seu código, `pausa_instrucao`), e comanda a ULA e a Memória para executar as tarefas decodificadas.

## 4. Conjunto de Instruções (ISA)
O simulador suporta um conjunto de instruções com múltiplos modos de endereçamento para flexibilidade.

| Mnemônico | Sintaxe(s) Suportada(s) | Descrição Detalhada |
| :--- | :--- | :--- |
| **LOAD** | `LOAD [reg], M(addr)`<br>`LOAD [reg], valor` | Carrega um valor para um registrador. A origem pode ser a Memória (Direto), um valor numérico (Imediato) ou outro Registrador. |
| **STOR** | `STOR M(addr), [reg]` | Armazena o valor de um registrador (padrão `AC`) em um endereço de memória. |
| **ADD** | `ADD [reg], M(addr)`<br>`ADD [reg], valor` | Soma um valor a um registrador (padrão `AC`) e atualiza as flags `Z` e `C`. |
| **SUB** | `SUB [reg], M(addr)`<br>`SUB [reg], valor` | Subtrai um valor a um registrador (padrão `AC`) e atualiza as flags `Z` e `C`. |
| **MULT** | `MULT M(addr)` | Multiplica o registrador `MQ` por um valor da memória. O resultado de 80 bits é salvo em `AC` (parte alta), `MQ` (parte baixa) we atualiza as flags `Z` e `C`. |
| **DIV** | `DIV M(addr)` | Divide o `AC` por um valor da memória, guardando o quociente em `MQ` e o resto em `AC`. |
| **MOV** | `MOV <reg_dest>, <reg_orig>` | Copia o valor de um registrador de origem para um de destino. |
| **JUMP** | `JUMP M(addr)` ou `JUMP addr` | Desvia incondicionalmente o fluxo do programa, alterando o `PC` para o endereço de destino. |
| **JUMP+** | `JUMP+ M(addr)` ou `JUMP+ addr`| Desvia o fluxo se o flag `Z` indicar que o último resultado foi positivo ou zero (`Z >= 0`). |
| **LSH** | `LSH` | Desloca os bits do `AC` uma posição para a esquerda (multiplicação por 2) e atualiza o flag `C`. |
| **RSH** | `RSH` | Desloca os bits do `AC` uma posição para a direita (divisão por 2) e atualiza o flag `C`. |

tem que arrumar os comandos que aceita
*Onde `[reg]` é opcional, o padrão é o Acumulador (`AC`).*

## 5. Como Executar o Simulador

### 5.1. Pré-requisitos
- Python 3.x instalado no sistema.

### 5.2. Passos para Execução
O programa é executado via terminal, especificando o algoritmo a ser testado.

1.  Garanta que os arquivos de programa (`fatorial.txt`, `selecao.txt`) estejam na mesma pasta que o script principal `Ciclo_instrucao.py`.
2.  Abra um terminal na pasta do projeto.
3.  Use um dos seguintes comandos:

    * **Para executar o algoritmo de Fatorial:**
        ```sh
        python Ciclo_instrucao.py -f pos_memoria
        ```
    * **Para executar o algoritmo de Selection Sort:**
        ```sh
        python Ciclo_instrucao.py -s pos_memoria
        ```

- A **flag** (`-f` ou `-s`) seleciona qual arquivo `.txt` será carregado.
- O **endereço hexadecimal** (`pos_memoria`) é o endereço inicial em que as instruções do programa serão carregadas na memória.

## 6. Formato do Arquivo de Entrada
O simulador lê arquivos `.txt` com a seguinte estrutura:

1.  **Seção de Dados:**
    As primeiras linhas são para inicializar a memória. O formato é `<valor_decimal> <endereco_hexadecimal>`.
    ```
    # Coloca o número 5 na posição 256 da memória.
    5 0x100
    ```
2.  **Linha em Branco:**
    Uma única linha em branco é usada para separar os dados das instruções.

3.  **Seção de Instruções:**
    As linhas restantes são as instruções do programa, que serão carregadas em sequência a partir do endereço inicial fornecido na linha de comando.
    ```
    # Carrega o valor do endereço 0x100 no Acumulador.
    LOAD AC, M(0x100)
    ```

## 7. Algoritmos Implementados
Para o trabalho, os seguintes algoritmos foram escritos em Assembly e estão disponíveis para teste:
- **`fatorial.txt`**: Calcula o fatorial de um número.
- **`selecao.txt`**: Ordena um vetor de números usando o método Selection Sort.
