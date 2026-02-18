#include <stdlib.h>
#include <stdio.h>

#define TAMANHO_MAXIMO 10

/* ========================================================================= */

typedef struct TipoCelula *TipoApontador;

typedef int TipoChave;

typedef struct TipoItem {
  TipoChave chave;
  /* outros componentes */
} TipoItem;

typedef struct TipoCelula {
  TipoItem item;
  TipoApontador proximo;
} TipoCelula;

typedef struct TipoFila {
  TipoApontador frente, tras;
} TipoFila;

/* ========================================================================= */

void Inicializa(TipoFila *fila){ 
  fila->frente = (TipoApontador) malloc(sizeof(TipoCelula));
  fila->tras = fila->frente;
  fila->frente->proximo = NULL;
} 

int Vazia(TipoFila fila){ 
  return (fila.frente == fila.tras); 
} 

void Enfileira(TipoItem elemento, TipoFila *fila){ 
  fila->tras->proximo = (TipoApontador) malloc(sizeof(TipoCelula));
  fila->tras = fila->tras->proximo;
  fila->tras->item = elemento;
  fila->tras->proximo = NULL;
} 

void Desenfileira(TipoFila *fila, TipoItem *elemento){ 
  TipoApontador p_auxiliar;

  if (Vazia(*fila)){ 
    printf("Erro! Fila esta vazia\n"); 
    return; 
  }

  p_auxiliar = fila->frente;
  fila->frente = fila->frente->proximo;
  *elemento = fila->frente->item;
  free(p_auxiliar);
} 

void Imprime(TipoFila fila){ 
  TipoApontador ponteiro;
  ponteiro = fila.frente->proximo;

  while (ponteiro != NULL) { 
    printf("%d\n", ponteiro->item.chave);
    ponteiro = ponteiro->proximo;
  }
}

/* ========================================================================= */

int main(int argc, char *argv[]){ 
  int vetor[TAMANHO_MAXIMO];
  int i, j, k, n;

  TipoFila fila;
  TipoItem item;

  Inicializa(&fila);
  
  /*Gera uma permutacao aleatoria de chaves entre 1 e MAX*/
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
  for (i = 0;i < TAMANHO_MAXIMO; i++){ 
    item.chave = vetor[i];
    Enfileira(item, &fila);
    printf("Enfileirou: %d \n", item.chave);
  }

  /*Desenfieleira cada chave */
  for (i = 0;i < TAMANHO_MAXIMO; i++){ 
   Desenfileira(&fila, &item);
   printf("Desenfileirou: %d \n", item.chave);
  }

  return 0;
}
