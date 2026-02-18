# 🤖 Resolvedor de Sudoku com IA (PSR)

Este projeto foi desenvolvido para a disciplina de **Introdução à Inteligência Artificial** e consiste na implementação de um resolvedor para uma variação do jogo **Sudoku 4x4**, modelado como um **Problema de Satisfação de Restrições (PSR)**.

O programa utiliza um algoritmo de **backtracking aprimorado** com heurísticas (_MRV_ e _Grau_) e a técnica de consistência de arco **AC-3** para encontrar soluções para diferentes instâncias do problema.

## 🚀 Tecnologias Utilizadas

- **Node.js:** Ambiente de execução para o código.
- **TypeScript:** Linguagem de programação principal.
- **Yarn** ou **npm:** Gerenciador de pacotes para as dependências do projeto.

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:

1.  **Node.js**: A versão do Node.js deve estar entre a **16** e a **22**.
    - Para verificar sua versão, rode no terminal: `node -v`
    - Caso não tenha instalado, baixe a versão LTS em [nodejs.org](https://nodejs.org/).
2.  **Yarn (Opcional)**: Se preferir usar o Yarn.
    - Caso não tenha, instale-o globalmente: `npm install -g yarn`

## 🛠️ Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente.

### Opção A: Se você baixou o projeto como `.zip` (ex: via e-mail)

1.  **Descompacte o arquivo** `IIA.SeuNomeSeuSobrenome.zip` em uma pasta de sua preferência.
2.  **Abra o terminal** e navegue até o diretório que você acabou de criar.
    ```bash
    cd caminho/para/a/pasta/do/projeto
    ```
3.  **Instale as dependências** usando `yarn` ou `npm`:

    ```bash
    # Usando Yarn
    yarn install

    # OU, usando npm
    npm install
    ```

### Opção B: Se você clonou o repositório Git

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```
2.  **Instale as dependências** usando `yarn` ou `npm`:

    ```bash
    # Usando Yarn
    yarn install

    # OU, usando npm
    npm install
    ```

## ▶️ Como Executar o Programa

Para iniciar o resolvedor, execute o seguinte comando na raiz do projeto:

  ```bash
    # Usando Yarn
    yarn start

    # OU, usando npm
    npm start
  ```

Ao executar o comando, um menu interativo aparecerá no seu terminal. Você deverá fazer 4 escolhas usando as setas do teclado e a tecla Enter:

- **Escolha o modo do problema:**
  - Parcial (5 variáveis), Completo (16 variáveis).
- **Escolha a instância de teste:**
  - Fácil, Média ou Difícil.
- **Escolha a heurística:**
  - Grau (Heurística de Grau) ou MRV (Valores Mínimos Restantes).
- **Deseja usar o pré-processamento AC-3?**
  - Yes (Sim) ou No (Não).

### 📄 Saída do Programa

O resultado da execução será exibido diretamente no terminal e também será salvo automaticamente em um arquivo de texto .txt dentro da pasta `output/`.

O nome do arquivo é gerado dinamicamente com base nas suas escolhas, seguindo o padrão:
`[instancia]_[heuristica]_[ac3 (opcional)].txt`

**Exemplo:** `easy_mrv_ac3.txt`

## 📂 Estrutura do Projeto
```bash
  src/
  ├── instances/    # Contém as instâncias do problema
  │   ├── full      # Arquivos .json com as instâncias do modo completo
  │   ├── partial   # Arquivos .json com as instâncias do modo parcial
  ├── model/        # Define a estrutura do problema (CSP) e suas restrições
  ├── shared/       # Módulos compartilhados pela aplicação
  │   ├── types.ts    # Definições de tipos e interfaces do TypeScript
  │   ├── utils.ts    # Funções e constantes utilitárias (ex: labels)
  │   └── reporter.ts # Responsável por formatar e salvar o relatório de saída
  ├── solver/       # Contém toda a lógica do resolvedor (backtracking, heurísticas, AC-3)
  └── main.ts       # Ponto de entrada do programa (executa o menu interativo)
```