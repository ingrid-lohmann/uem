#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ORDEM 5

// Estrutura para representar uma chave-offset
struct chave_offset
{
  int chave;
  int offset;
};

// Estrutura para representar uma página de árvore-B
struct pagina
{
  int chaves_por_pagina;
  struct chave_offset chaves[ORDEM];
  int filhos[ORDEM + 1];
};

// Estrutura para representar um registro de árvore-B
struct registro
{
  int identificador;
  char titulo[50];
  int ano;
  char genero[20];
  char publicadora[20];
  char plataforma[20];
  int tamanho;
};

// Função para ler um arquivo de registros
int ler_registros(char *arquivo_dados, struct registro *registros)
{
  FILE *arquivo = fopen(arquivo_dados, "rb");
  if (arquivo == NULL)
  {
    printf("Erro ao abrir o arquivo de dados: %s\n", arquivo_dados);
    return -1;
  }

  int total_registros;
  fread(&total_registros, sizeof(int), 1, arquivo);

  for (int i = 0; i < total_registros; i++)
  {
    struct registro registro;
    fread(&registro, sizeof(struct registro), 1, arquivo);
    registros[i] = registro;
  }

  fclose(arquivo);
  return total_registros;
}

// Função para criar uma nova página de árvore-B
struct pagina *nova_pagina()
{
  struct pagina *pagina = malloc(sizeof(struct pagina));
  pagina->chaves_por_pagina = 0;
  return pagina;
}

int inserir_chave_offset(struct pagina *pagina, int chave, int offset)
{
  // Se a página for nula, crie uma nova página
  if (pagina == NULL)
  {
    return -1;
  }

  // Encontre o local correto para inserir a chave
  int i;
  for (i = 0; i < pagina->chaves_por_pagina; i++)
  {
    if (pagina->chaves[i].chave > chave)
    {
      break;
    }
  }

  // Se a chave já existe, retorne
  for (int j = 0; j < pagina->chaves_por_pagina; j++)
  {
    if (pagina->chaves[j].chave == chave)
    {
      return -1;
    }
  }

  // Mova as chaves posteriores para a direita
  for (int j = pagina->chaves_por_pagina; j > i; j--)
  {
    pagina->chaves[j] = pagina->chaves[j - 1];
    pagina->filhos[j] = pagina->filhos[j - 1];
  }

  // Insira a nova chave
  pagina->chaves[i].chave = chave;
  pagina->chaves[i].offset = offset;
  pagina->chaves_por_pagina++;

  // Se a página estiver cheia, divida-a
  if (pagina->chaves_por_pagina == ORDEM)
  {
    // Crie uma nova página
    struct pagina *nova_pagina = malloc(sizeof(struct pagina));

    // Mova metade das chaves para a nova página
    for (int j = 0; j < ORDEM / 2; j++)
    {
      nova_pagina->chaves[j] = pagina->chaves[ORDEM - j - 1];
      nova_pagina->filhos[j] = pagina->filhos[ORDEM - j - 1];
    }

    // Atualize as chaves e filhos da página original
    pagina->chaves_por_pagina = ORDEM / 2;
    pagina->filhos[ORDEM] = nova_pagina->chaves_por_pagina + 1;

    // Retorne o índice da nova página
    return nova_pagina->chaves_por_pagina + 1;
  }

  // Retorne o número de chaves na página
  return pagina->chaves_por_pagina;
}

// Função para buscar uma chave em uma árvore-B
struct chave_offset *buscar_chave(struct pagina *pagina, int chave)
{
  // Se a página for nula, a chave não foi encontrada
  if (pagina == NULL)
  {
    return NULL;
  }

  // Encontre a chave na página
  for (int i = 0; i < pagina->chaves_por_pagina; i++)
  {
    if (pagina->chaves[i].chave == chave)
    {
      return &pagina->chaves[i];
    }
  }

  // A chave não foi encontrada na página
  return NULL;
}

// Função para imprimir uma subárvore
// void imprimir_subarvore(struct pagina *pagina)
// {
//   // Se a página for nula, não há nada a imprimir
//   if (pagina == NULL)
//   {
//     return;
//   }

//   // Imprima a página
//   printf("Pagina %d:\n", pagina->chaves_por_pagina);

//   for (int i = 0; i < pagina->chaves_por_pagina; i++)
//   {
//     printf("  Chave %d: %d\n", i + 1, pagina->chaves[i].chave);
//   }

//   // Imprima as subárvores
//   for (int i = 0; i <= pagina->chaves_por_pagina; i++)
//   {
//     imprimir_subarvore(pagina->filhos[i]);
//   }
// }

// Função para imprimir uma árvore-B
// void imprimir_arvore(struct pagina *pagina)
// {
//   // Se a página for nula, não há nada a imprimir
//   if (pagina == NULL)
//   {
//     return;
//   }

//   // Imprima a subárvore
//   imprimir_subarvore(pagina);
// }

// Função para criar o índice
struct pagina *criar_indice()
{
  // Leia os registros do arquivo de dados
  struct registro *registros;
  int total_registros = ler_registros("dados.dat", registros);

  // Crie a página raiz
  struct pagina *pagina_raiz = nova_pagina();

  // Insira as chaves dos registros na árvore
  for (int i = 0; i < total_registros; i++)
  {
    inserir_chave_offset(pagina_raiz, registros[i].identificador, i);
  }

  return pagina_raiz;
}

// Função para executar as operações do arquivo
void exec_arquivo_operacoes(char *argv)
{
  struct pagina *pagina_raiz = NULL;

  printf("%s", argv);

  // Abra o arquivo de operações
  FILE *arquivo = fopen(argv, "r");

  if (arquivo == NULL)
  {
    printf("Erro ao abrir o arquivo de operações: %s\n", argv);
    return;
  }

  // Leia as operações do arquivo
  char linha[100];
  while (fgets(linha, sizeof(linha), arquivo) != NULL)
  {
    // Limpe o final da linha
    linha[strcspn(linha, "\n")] = '\0';

    // Ignorar linhas em branco
    if (linha[0] == '\0')
    {
      continue;
    }

    // Executar a operação
    int chave;
    int offset;
    char comando[10];
    sscanf(linha, "%s %d %d", comando, &chave, &offset);

    if (strcmp(comando, "inserir") == 0)
    {
      // Insira a chave no índice
      inserir_chave_offset(pagina_raiz, chave, offset);
    }
    else if (strcmp(comando, "buscar") == 0)
    {
      // Busque a chave no índice
      struct chave_offset *chave_offset = buscar_chave(pagina_raiz, chave);
      if (chave_offset == NULL)
      {
        printf("Chave não encontrada\n");
      }
      else
      {
        printf("Chave encontrada no offset %d\n", chave_offset->offset);
      }
    }
    else
    {
      printf("Comando inválido: %s\n", comando);
    }
  }

  // Feche o arquivo de operações
  fclose(arquivo);
}

// Função principal
int main(int argc, char *argv[])
{
  // struct pagina *pagina_raiz = NULL;

  struct pagina *pagina_raiz = criar_indice();

  printf("%s", argv);
  printf("%s", argv[2]);

  // Verifica se o número de parâmetros é correto
  if (argc != 2)
  {
    printf("Uso: %s [-c | -e | -p]\n", argv[0]);
    return 1;
  }

  // Verifica a operação a ser executada
  if (strcmp(argv[1], "-c") == 0)
  {
    // Cria o índice
    pagina_raiz = criar_indice();
  }
  else if (argc == 3 && (strcmp(argv[1], "-e")) == 0)
  {
    // Executa as operações do arquivo
    exec_arquivo_operacoes(argv[2]);
  }
  else if (strcmp(argv[1], "-p") == 0)
  {
    // Imprime as informações da árvore
    // imprimir_arvore(pagina_raiz);
    printf("imprimiu");
  }
  else
  {
    // Operação inválida
    printf("Operação inválida: %s\n", argv[1]);
    return 1;
  }

  return 0;
}

// gcc -o arvore-b nova.c

// int main(int argc, char *argv[])
// {
//   struct pagina *pagina_raiz = criar_indice();

//   if (strcmp(argv[1], "-c") == 0)
//   {
//     // Cria o índice
//     pagina_raiz = criar_indice();
//   }

//   if (argc == 3 && strcmp(argv[1], "-e") == 0)
//   {
//     printf("Execução de operações ativo...Arquivo = %s\n", argv[2]);
//     exec_arquivo_operacoes(argv[2]);
//   }
//   else if (argc == 2 && strcmp(argv[1], "-p") == 0)
//   {
//     printf("Imprimindo a LED...Pro favor aguarde.\n");
//     // imprimirLed();
//   }
//   else
//   {
//     fprintf(stderr, "Argumentos incorretos!\n");
//     fprintf(stderr, "Modo de uso:\n");
//     fprintf(stderr, "$ %s (-i|-e) nome_arquivo\n", argv[0]);
//     fprintf(stderr, "$ %s -p\n", argv[0]);
//     exit(EXIT_FAILURE);
//   }

//   return 0;
// }