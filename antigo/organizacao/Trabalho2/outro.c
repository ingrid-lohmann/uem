#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ORDEM 5

typedef struct Pagina
{
  int rrn;
  int n;
  int chaves[ORDEM - 1];
  int byte_offsets[ORDEM - 1];
  int filhos[ORDEM];
} Pagina;

struct registro
{
  int identificador;
  char nome[32];
  int ano;
  char genero[32];
  char desenvolvedora[32];
  char plataforma[32];
};

void imprime_pagina(Pagina *pagina)
{
  printf("Página %d\n", pagina->rrn);
  printf("Chaves: ");
  for (int i = 0; i < pagina->n; i++)
  {
    printf("%d ", pagina->chaves[i]);
  }
  printf("\nOffsets: ");
  for (int i = 0; i < pagina->n; i++)
  {
    printf("%d ", pagina->byte_offsets[i]);
  }
  printf("\nFilhas: ");
  for (int i = 0; i < ORDEM; i++)
  {
    printf("%d ", pagina->filhos[i]);
  }
  printf("\n");
}

int le_arquivo_dados(char *nome_arquivo, Pagina **paginas)
{
  FILE *arquivo = fopen(nome_arquivo, "rb");
  if (arquivo == NULL)
  {
    return -1;
  }

  // Lê o número de registros no arquivo.

  int n_registros;
  fread(&n_registros, sizeof(int), 1, arquivo);

  // Aloca memória para as páginas.

  int n_paginas = (n_registros + ORDEM - 1) / ORDEM;
  *paginas = malloc(sizeof(Pagina) * n_paginas);
  if (*paginas == NULL)
  {
    return -1;
  }

  // Lê os registros do arquivo.

  for (int i = 0; i < n_registros; i++)
  {
    int identificador, byte_offset;
    fread(&identificador, sizeof(int), 1, arquivo);
    fread(&byte_offset, sizeof(int), 1, arquivo);

    // Insere o registro na árvore.

    Pagina *pagina = &(*paginas)[i / ORDEM];
    insere_registro(pagina, identificador, byte_offset);
  }

  fclose(arquivo);
  return n_paginas;
}

void insere_registro(Pagina *pagina, int identificador, int byte_offset)
{
  // Encontra a posição da chave no vetor de chaves.

  int i;
  for (i = 0; i < pagina->n; i++)
  {
    if (pagina->chaves[i] > identificador)
    {
      break;
    }
  }

  // Move as chaves para a direita.

  for (int j = pagina->n - 1; j >= i; j--)
  {
    pagina->chaves[j + 1] = pagina->chaves[j];
    pagina->byte_offsets[j + 1] = pagina->byte_offsets[j];
  }

  // Insere a nova chave e o byte-offset.

  pagina->chaves[i] = identificador;
  pagina->byte_offsets[i] = byte_offset;

  // Se necessário, divide a página.

  if (pagina->n == ORDEM)
  {
    int filho_meio = (pagina->n - 1) / 2;
    Pagina *pagina_nova = malloc(sizeof(Pagina));
    pagina_nova->rrn = pagina->rrn + 1;
    pagina_nova->n = pagina->n - filho_meio - 1;
    memcpy(pagina_nova->chaves, pagina->chaves + filho_meio + 1, sizeof(int) * pagina_nova->n);
    memcpy(pagina_nova->byte_offsets, pagina->byte_offsets + filho_meio + 1, sizeof(int) * pagina_nova->n);
    pagina->n = filho_meio;
    pagina->filhos[filho_meio] = pagina_nova->rrn;
  }
}

// Função para buscar uma chave em uma árvore-B
int busca(Pagina *pagina, int identificador)
{
  // Encontra a página que contém a chave.

  Pagina *paginas = &paginas[0];
  while (pagina->n > 0 && pagina->chaves[0] < identificador)
  {
    pagina = &paginas[pagina->filhos[0]];
  }

  // Verifica se a chave está na página.

  for (int i = 0; i < pagina->n; i++)
  {
    if (pagina->chaves[i] == identificador)
    {
      return pagina->byte_offsets[i];
    }
  }
  // A chave não foi encontrada.
  return -1;
}

int main(int argc, char *argv[])
{
  typedef struct registro registro_t;

  registro_t registro;

  int *registro_ptr = (int *)registro;
  // Verifica a quantidade de argumentos
  if (argc < 2)
  {
    printf("Uso: %s <opção> [argumentos]\n", argv[0]);
    return 1;
  }

  // Obtém a opção
  char *opcao = argv[1];

  // Cria o arquivo de dados
  char *dados_dat = "dados.dat";
  FILE *f_dados = fopen(dados_dat, "wb");
  if (f_dados == NULL)
  {
    printf("Erro ao criar o arquivo de dados.\n");
    return 1;
  }

  // Cria o arquivo de índice
  char *btree_dat = "btree.dat";
  FILE *f_btree = fopen(btree_dat, "wb");
  if (f_btree == NULL)
  {
    printf("Erro ao criar o arquivo de índice.\n");
    return 1;
  }

  // Realiza a operação solicitada
  if (strcmp(opcao, "c") == 0)
  {
    // Cria o índice
    int ret = criar_indice(dados_dat, btree_dat);
    if (ret != 0)
    {
      printf("Erro ao criar o índice.\n");
      return 1;
    }
    printf("Índice criado com sucesso.\n");
  }
  else if (strcmp(opcao, "b") == 0)
  {
    // Busca um registro
    int chave = atoi(argv[2]);
    registro_t registro = NULL;
    registro = buscar_registro(chave, dados_dat, btree_dat);
    if (registro == NULL)
    {
      printf("Registro não encontrado.\n");
    }
    else
    {
      printf("Registro encontrado:\n");
      printf("%d|%s|%d|%s|%s|%s\n", *(int *)registro, registro->nome, registro->ano,
             registro->genero, registro->desenvolvedora, registro->plataforma);
    }
  }
  else if (strcmp(opcao, "i") == 0)
  {
    // Insere um registro
    int chave = atoi(argv[2]);
    int ret = inserir_registro(chave, dados_dat, btree_dat);
    if (ret != 0)
    {
      printf("Erro ao inserir o registro.\n");
    }
    else
    {
      printf("Registro inserido com sucesso.\n");
    }
  }
  else
  {
    // Operação inválida
    printf("Opção inválida.\n");
    return 1;
  }

  // Fecha os arquivos
  fclose(f_dados);
  fclose(f_btree);

  return 0;
}
