struct pagina
{
  int chaves_por_pagina;
  struct chave
  {
    int chave;
    int offset;
  } chaves[MAX_CHAVES_POR_PAGINA];
};

/*
Essa estrutura define uma página de árvore-b com um número máximo de chaves. Cada chave é composta por um valor e um offset, que indica a posição do dado armazenado na página.

Para inserir um dado na árvore-b, você pode seguir esses passos:

Encontre a página que deve conter a chave do dado.
Se a página não estiver cheia, insira a chave na página.
Se a página estiver cheia, divida a página em duas e mova metade das chaves para a nova página.
Para pesquisar um dado na árvore-b, você pode seguir esses passos:

Comece na raiz da árvore.
Compare a chave do dado com a chave da primeira chave da página.
Se as chaves forem iguais, retorne o offset do dado.
Se as chaves não forem iguais, siga a página que aponta a chave menor que a chave do dado.
Repita os passos 2 a 4 até encontrar o dado ou chegar a uma página vazia.
Aqui está um exemplo de como você pode inserir um dado na árvore-b:
*/

int inserir_dado(struct pagina *pagina, int chave, int offset)
{
  int i;

  for (i = 0; i < pagina->chaves_por_pagina; i++)
  {
    if (pagina->chaves[i].chave == chave)
    {
      return -1;
    }

    if (pagina->chaves[i].chave > chave)
    {
      break;
    }
  }

  if (pagina->chaves_por_pagina < MAX_CHAVES_POR_PAGINA)
  {
    pagina->chaves[i].chave = chave;
    pagina->chaves[i].offset = offset;
    pagina->chaves_por_pagina++;
    return 0;
  }
  else
  {
    struct pagina *nova_pagina = malloc(sizeof(struct pagina));
    for (i = pagina->chaves_por_pagina / 2; i < pagina->chaves_por_pagina; i++)
    {
      nova_pagina->chaves[i - pagina->chaves_por_pagina / 2].chave = pagina->chaves[i].chave;
      nova_pagina->chaves[i - pagina->chaves_por_pagina / 2].offset = pagina->chaves[i].offset;
    }
    nova_pagina->chaves_por_pagina = pagina->chaves_por_pagina - pagina->chaves_por_pagina / 2;
    pagina->chaves_por_pagina = pagina->chaves_por_pagina / 2;
    pagina->chaves[pagina->chaves_por_pagina].chave = chave;
    pagina->chaves[pagina->chaves_por_pagina].offset = offset;
    pagina->chaves_por_pagina++;
    return inserir_dado(nova_pagina, nova_pagina->chaves[0].chave, nova_pagina->chaves[0].offset);
  }
}

/*
Este código funciona da seguinte forma:

O loop for percorre todas as chaves da página.
Se a chave do dado já existe na página, a função retorna -1.
Se a chave do dado é menor que a primeira chave da página, a função insere a chave na primeira posição da página.
Se a chave do dado é maior que a última chave da página, a função insere a chave na última posição da página.
Se a chave do dado está entre duas chaves da página, a função insere a chave na posição correta.
Se a página está cheia, a função divide a página em duas e move metade das chaves para a nova página.
A função chama a si mesma para inserir a chave na nova página.
*/

int buscar_dado(struct pagina *raiz, int chave)
{
  while (raiz != NULL)
  {
    int i;

    for (i = 0; i < raiz->chaves_por_pagina; i++)
    {
      if (raiz->chaves[i].chave == chave)
      {
        return raiz->chaves[i].offset;
      }

      if (raiz->chaves[i].chave > chave)
      {
        raiz = raiz->chaves[i].filho;
        break;
      }
    }

    if (i == raiz->chaves_por_pagina)
    {
      raiz = raiz->filhos[raiz->chaves_por_pagina];
    }
  }

  return -1;
}

// Aqui está um exemplo de como você pode usar essa função para buscar um dado:

int chave = 10;
int offset = buscar_dado(raiz, chave);

if (offset != -1)
{
  // O registro foi encontrado.
  // Acesse o registro a partir do offset.
}
else
{
  // O registro não foi encontrado.
}

// Para acessar o registro diretamente no arquivo dados.dat, você pode usar o seguinte código:

int chave = 10;
int offset = buscar_dado(raiz, chave);

if (offset != -1)
{
  // Acesse o registro a partir do offset.
  // Por exemplo, se o arquivo dados.dat for um arquivo binário, você pode usar a seguinte função para acessar o registro:
  struct registro *registro = (struct registro *)malloc(sizeof(struct registro));
  fread(registro, sizeof(struct registro), 1, dados.dat + offset);

  // Processe o registro.
}
else
{
  // O registro não foi encontrado.
}

// Este código abre o arquivo dados.dat e lê o registro a partir do offset. O registro é então alocado na memória e o código pode processá-lo.

void imprimir_arvore(struct pagina *raiz)
{
  if (raiz == NULL)
  {
    return;
  }

  printf("Página %d:\n", raiz->chaves_por_pagina);
  printf("Chaves:\n");
  for (int i = 0; i < raiz->chaves_por_pagina; i++)
  {
    printf("\t%d\n", raiz->chaves[i].chave);
  }
  printf("Offsets:\n");
  for (int i = 0; i < raiz->chaves_por_pagina; i++)
  {
    printf("\t%d\n", raiz->chaves[i].offset);
  }
  printf("Filhas:\n");
  for (int i = 0; i <= raiz->chaves_por_pagina; i++)
  {
    printf("\t%d\n", raiz->filhos[i]);
  }

  imprimir_arvore(raiz->filhos[0]);
  for (int i = 1; i < raiz->chaves_por_pagina; i++)
  {
    imprimir_arvore(raiz->filhos[i]);
  }
}

/*
Este código funciona da seguinte forma:

A função começa na raiz da árvore.
A função imprime o número de chaves da página.
A função imprime todas as chaves da página.
A função imprime todos os offsets das chaves da página.
A função imprime todos os ponteiros para as filhas da página.
A função chama a si mesma para imprimir as informações das páginas filhas.
Aqui está um exemplo de como você pode usar essa função para imprimir as informações da árvore-b:
*/

struct pagina *raiz = ...;

imprimir_arvore(raiz);

/*
Este código imprimirá as informações de todas as páginas da árvore-b.

Você pode modificar esse código para imprimir as informações de forma mais detalhada, por exemplo, incluindo o tamanho da página, o número de filhos de cada página, etc.
*/

int main(int argc, char *argv[])
{
  if (argc == 3 && strcmp(argv[1], "-e") == 0)
  {
    printf("Execução de operações ativo...Arquivo = %s\n", argv[2]);
    executarOperacoes(argv[2]);
  }
  else if (argc == 2 && strcmp(argv[1], "-p") == 0)
  {
    printf("Imprimindo a LED...Pro favor aguarde.\n");
    imprimir_arvore();
  }
  else
  {
    fprintf(stderr, "Argumentos incorretos!\n");
    fprintf(stderr, "Modo de uso:\n");
    fprintf(stderr, "$ %s (-i|-e) nome_arquivo\n", argv[0]);
    fprintf(stderr, "$ %s -p\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  return 0;
}