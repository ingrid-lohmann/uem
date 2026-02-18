#include <stdlib.h>
#include <stdio.h>

#define TAMANHO_MAXIMO 10

/* ========================================================================= */

typedef struct TipoItem *TipoApontador;

typedef struct TipoItem {
  TipoApontador anterior;
  int conteudo;
  TipoApontador proximo;
} TipoItem;

typedef struct {
  TipoApontador primeiro, ultimo;
} TipoLista;

/* ========================================================================= */

void Inicializa(TipoLista *lista){ 
  lista->primeiro = (TipoApontador) malloc (sizeof(TipoItem));
  lista->primeiro->anterior = NULL;
  lista->primeiro->proximo = NULL;
  lista->ultimo = lista->primeiro;
}

int Vazia(TipoLista lista){ 
  return (lista.primeiro == lista.ultimo);
}

void Insere(int elemento, TipoLista *lista){ 
  lista->ultimo->proximo = (TipoApontador) malloc(sizeof(TipoItem));
  lista->ultimo->proximo->anterior = lista->ultimo->proximo;

  lista->ultimo = lista->ultimo->proximo;
  lista->ultimo->conteudo = elemento;
  lista->ultimo->proximo = NULL;
}

void Retira(TipoApontador ponteiro, TipoLista *lista, int elemento){ 
  TipoApontador p_auxiliar;

  if (Vazia(*lista) || ponteiro == NULL || ponteiro->proximo == NULL) { 
    printf(" Erro! Lista vazia ou posicao nao existe \n");
    return;
  }

  p_auxiliar = ponteiro->proximo;
  elemento = p_auxiliar->conteudo;

  if (p_auxiliar->proximo != NULL){
    p_auxiliar->proximo->anterior = p_auxiliar->anterior;
    ponteiro->proximo = p_auxiliar->proximo;
    p_auxiliar->anterior = NULL;
    p_auxiliar->proximo = NULL;
  }else{
    lista->ultimo = p_auxiliar->anterior;
    lista->ultimo->proximo = NULL;    
    ponteiro->proximo = NULL;
    p_auxiliar->anterior = NULL;
  }
  free(p_auxiliar);
}

void Imprime(TipoLista lista){ 
  TipoApontador p_auxiliar;
  p_auxiliar = lista.primeiro->proximo;

  while (p_auxiliar != NULL) { 
    printf("%d\n", p_auxiliar->conteudo);
    p_auxiliar = p_auxiliar->proximo;
  }
}

/* ========================================================================== */

int main(int argc, char *argv[]){ 
  int i, j, k, n;
  int vetor[TAMANHO_MAXIMO];
  float  tamanho;     

  TipoApontador ponteiro;
  TipoLista lista;
  int elemento;
  
  tamanho = 0;
  Inicializa(&lista);

  /*Gera uma permutacao aleatoria de chaves entre 1 e MAXIMO*/
  for(i = 0; i < TAMANHO_MAXIMO; i++) 
    vetor[i] = i + 1;

  for(i = 0; i < TAMANHO_MAXIMO; i++){ 
    k =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
    j =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
    n = vetor[k];
    vetor[k] = vetor[j];
    vetor[j] = n;
  }

  /*Insere cada chave na lista */
  for (i = 0; i < TAMANHO_MAXIMO; i++){ 
    elemento = vetor[i];
    Insere(elemento, &lista);
    tamanho++;
  }
  Imprime(lista);

  /*Retira cada chave da lista */
  for(i = 0; i < TAMANHO_MAXIMO; i++){ /*escolhe uma chave aleatoriamente */
    k = (int) ((tamanho) * rand() / (RAND_MAX + 1.0));
    ponteiro = lista.primeiro;
    /*retira chave apontada */
    Retira(ponteiro, &lista, elemento);
    tamanho--;
  }
  printf("\n Lista Final \n");
  Imprime (lista);
  return(0);
}
