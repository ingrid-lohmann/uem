#include <stdio.h>
#include <stdlib.h>

#define TAMANHO_MAXIMO 10

/* ========================================================================= */

typedef int TipoChave;

typedef struct{
  int chave;
  /* --- outros componentes podem ser adicionados na estrutura --- */
} TipoItem;

typedef struct TipoCelula *TipoApontador;

typedef struct TipoCelula {
  TipoItem item;
  TipoApontador proximo;
} TipoCelula;

typedef struct {
  int tamanho;
  TipoApontador fundo, topo;
} TipoPilha;

/* ========================================================================= */

void Inicializa(TipoPilha *pilha){ 
  pilha->topo = (TipoApontador) malloc(sizeof(TipoCelula));
  pilha->fundo = pilha->topo;
  pilha->topo->proximo = NULL;
  pilha->tamanho = 0;
} 

int Vazia(TipoPilha pilha){ 
  return (pilha.topo == pilha.fundo); 
} 

void Empilha(TipoItem elemento, TipoPilha *pilha){ 
  TipoApontador p_auxiliar;
  p_auxiliar = (TipoApontador) malloc(sizeof(TipoCelula));
  pilha->topo->item = elemento;
  p_auxiliar->proximo = pilha->topo;
  pilha->topo = p_auxiliar;
  pilha->tamanho++;
} 

void Desempilha(TipoPilha *pilha, TipoItem *item){ 
  TipoApontador p_auxiliar;

  if (Vazia(*pilha)){ 
    printf("Erro: pilha vazia\n"); 
    return; 
  }

  p_auxiliar = pilha->topo;
  pilha->topo = p_auxiliar->proximo;
  *item = p_auxiliar->proximo->item;
  free(p_auxiliar);  
  pilha->tamanho--;
} 

int Tamanho(TipoPilha pilha){ 
  return (pilha.tamanho); 
} 

/* ========================================================================= */

int main(int argc, char *argv[]){ 
  TipoPilha pilha;
  TipoItem item;
  int vetor[TAMANHO_MAXIMO];
  int i, j, k, n;
 
  Inicializa(&pilha);
  
  /*Gera uma permutacao aleatoria de chaves entre 1 e MAXIMO*/
  for(i = 0; i < TAMANHO_MAXIMO; i++) 
    vetor[i] = i + 1;

  for(i = 0; i < TAMANHO_MAXIMO; i++){ 
    k =  (int) (10.0*rand()/(RAND_MAX + 1.0));
    j =  (int) (10.0*rand()/(RAND_MAX + 1.0));
    n = vetor[k];
    vetor[k] = vetor[j];
    vetor[j] = n;
  }
  
  /*Empilha cada chave */
  for (i = 0; i < TAMANHO_MAXIMO; i++){ 
    item.chave = vetor[i];
    Empilha(item, &pilha);
    printf("Empilhou: %d \n", item.chave);
  }

  printf("Tamanho da pilha: %d \n", Tamanho(pilha));
  
  /*Desempilha cada chave */
  for(i = 0; i < TAMANHO_MAXIMO; i++){ 
    Desempilha (&pilha,&item);
      printf ("Desempilhou: %d \n", item.chave);
  }
 
  printf("Tamanho da pilha: %d\n", Tamanho(pilha));
  return(0);
}
