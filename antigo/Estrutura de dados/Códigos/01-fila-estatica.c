#include <stdio.h>
#include <stdlib.h>

#define TAMANHO_MAXIMO  1000

/* ========================================================================= */

typedef int TipoApontador;

typedef int TipoChave;

typedef struct {
  TipoChave chave;
  /* --- outros componentes podem ser adicionados na estrutura --- */
} TipoItem;

typedef struct {
  TipoItem item[TAMANHO_MAXIMO];
  TipoApontador frente, tras;
} TipoFila;

/* ========================================================================= */

void Inicializa(TipoFila *fila){ 
  fila->frente = 1;
  fila->tras = fila->frente;
} 

int Vazia(TipoFila fila){ 
  return (fila.frente == fila.tras); 
} 

void Enfileira(TipoItem elemento, TipoFila *fila){ 
  if (fila->tras % TAMANHO_MAXIMO + 1 == fila->frente)
    printf(" Erro! Fila Cheia \n");
  else{ 
    fila->item[fila->tras] = elemento;
    fila->tras = fila->tras % TAMANHO_MAXIMO + 1;
  }
} 

void Desenfileira(TipoFila *fila, TipoItem *elemento){ 
  if(Vazia(*fila))
    printf("Erro! Fila esta vazia\n");
  else{ 
    *elemento = fila->item[fila->frente];
    fila->frente = fila->frente % TAMANHO_MAXIMO + 1;
  }
} 

void Imprime(TipoFila fila){ 
  int indice;

  for (indice = fila.frente; indice < fila.tras; indice++)
    printf("%d\n", fila.item[indice].chave);
}

/* ========================================================================= */

int main(int argc, char *argv[]){ 
  int vetor[TAMANHO_MAXIMO];
  int i, j, k, n, tamanho;

  TipoFila fila;
  TipoItem item;

  tamanho = 10;
  Inicializa(&fila);
  
  /*Gera uma permutacao aleatoria de chaves entre 1 e max*/
  for(i = 0; i < tamanho; i++) 
    vetor[i] = i + 1;

  for(i = 0; i < tamanho; i++){ 
    k =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
    j =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
    n = vetor[k];
    vetor[k] = vetor[j];
    vetor[j] = n;
  }

  /*Enfileira  cada chave  */
  for (i = 0; i < tamanho; i++){ 
    item.chave = vetor[i];
    Enfileira(item, &fila);
    printf("Enfileirou: %d \n", item.chave);
  }
  
  /*Desenfileira cada chave */
  for(i = 0; i < tamanho; i++){ 
    Desenfileira(&fila, &item);
    printf("Desenfileirou: %d\n", item.chave);
  }

  return(0);
}
