#include <stdio.h>
#include <stdlib.h>

#define TAMANHO_MAXIMO 1000

/* ========================================================================= */

typedef int TipoApontador;

typedef int TipoChave;

typedef struct{
  TipoChave chave;
  /* --- outros componentes podem ser adicionados na estrutura --- */
} TipoItem;

typedef struct{
  TipoItem item[TAMANHO_MAXIMO];
  TipoApontador topo;
} TipoPilha;

/* ========================================================================= */

void Inicializa(TipoPilha *pilha){ 
  pilha->topo = 0; 
} 

int Vazia(TipoPilha pilha){ 
  return (pilha.topo == 0); 
} 

void Empilha(TipoItem elemento, TipoPilha *pilha){ 
  if (pilha->topo == TAMANHO_MAXIMO) 
    printf(" Erro! Pilha cheia \n");
  else{ 
    pilha->topo++; 
    pilha->item[pilha->topo - 1] = elemento; 
  }
} 

void Desempilha(TipoPilha *pilha, TipoItem *elemento){ 
  if (Vazia(*pilha)) 
    printf(" Erro! Pilha vazia \n");
  else{ 
    *elemento = pilha->item[pilha->topo - 1]; 
    pilha->topo--; 
  }
} 

int Tamanho(TipoPilha pilha){ 
  return (pilha.topo); 
}  

/* ========================================================================= */

int  main(int argc, char *argv[]){ 
  int vetor[TAMANHO_MAXIMO];
  int i, j, k, n, tamanho;

  TipoPilha pilha;
  TipoItem item;

  tamanho = 10;
  Inicializa(&pilha);
  
  /*Gera uma permutacao aleatoria de chaves entre 1 e maximo*/
  for(i = 0; i < tamanho; i++) 
    vetor[i] = i + 1;

  for(i = 0; i < tamanho; i++){ 
    k =  (int) (10.0*rand()/(RAND_MAX + 1.0));
    j =  (int) (10.0*rand()/(RAND_MAX + 1.0));
    n = vetor[k];
    vetor[k] = vetor[j];
    vetor[j] = n;
  }
  
/*Insere cada chave na lista */
  for (i = 0; i < tamanho; i++){ 
    item.chave = vetor[i];
    Empilha(item, &pilha);
    printf("Empilhou: %d \n", item.chave);
  }
  
  printf("Tamanho da pilha: %d\n", Tamanho(pilha));

  /*Desempilha cada chave */
  for(i = 0; i < tamanho; i++){ 
    Desempilha(&pilha, &item);
      printf ("Desempilhou: %d\n", item.chave);
  }
  printf ("Tamanho da pilha: %d \n", Tamanho(pilha));
  return(0);
}
