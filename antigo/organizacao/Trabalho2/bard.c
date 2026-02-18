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

// Função para inserir uma chave-offset em uma página de árvore-B
int inserir_chave_offset(struct pagina *pagina, int chave, int offset)
{
  int i;

  // Encontre o local correto para inserir a chave
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
    struct pagina *nova_pagina = malloc(sizeof(struct pagina));

    // Mova metade das chaves para a nova página
    for (int j = 0; j < ORDEM / 2; j++)
    {
      nova_pagina->chaves[j] = pagina->chaves[ORDEM - j - 1];
      nova_pagina->filhos[j] = pagina->filhos[ORDEM - j];
    }

    // Atualize as chaves e filhos da página original
    pagina->chaves_por_pagina = ORDEM / 2;
    pagina->filhos[ORDEM] = nova_pagina->chaves_por_pagina + 1;

    return nova_pagina->chaves_por_pagina + 1;
  }

  return 1;
}

// Função para buscar uma chave em uma árvore-B
int buscar_chave(struct pagina *pagina, int chave)
{
  if (pagina == NULL)
  {
    return -1;
  }

  for (int i = 0; i < pagina->chaves_por_pagina; i++)
  {
    if (pagina->chaves[i].chave == chave)
    {
      return pagina->chaves[i].offset;
    }

    if (pagina->chaves[i].chave > chave)
    {
      return buscar_chave(pagina->filhos[i], chave);
    }
  }

  return -1;
}

// Função para imprimir uma árvore-B
void imprimir_arvore(struct pagina *pagina)
{
  if (pagina == NULL)
  {
    return;
  }

  printf("Pagina %d:\n", pagina->chaves_por_pagina);

  for (int i = 0; i < pagina->chaves_por_pagina; i++)
  {
    printf("  Chave %d: %d\n", i + 1, pagina->chaves[i].chave);
  }

  for (int i = 0; i <= pagina->chaves_por_pagina; i++)
  {
    imprimir_arvore(pagina->filhos[i]);
  }
}

int main(int argc, char *argv[])
{
  struct pagina *pagina_raiz = NULL;
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
    criar_indice();
  }
  else if (strcmp(argv[1], "-e") == 0)
  {
    // Executa as operações do arquivo
    exec_arquivo_operacoes(argv[2]);
  }
  else if (strcmp(argv[1], "-p") == 0)
  {
    // Imprime as informações da árvore
    imprimir_arvore(pagina_raiz);
  }
  else
  {
    // Operação inválida
    printf("Operação inválida: %s\n", argv[1]);
    return 1;
  }

  return 0;
}
