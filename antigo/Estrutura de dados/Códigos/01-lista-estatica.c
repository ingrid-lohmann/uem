#include <stdio.h>
#include <stdlib.h>

#define INICIO_ARRANJO  0
#define TAMANHO_MAXIMO  1000

/* ========================================================================= */

typedef int TipoChave;

typedef int TipoApontador;

typedef struct {
  TipoChave chave;
  /* --- outros componentes podem ser adicionados na estrutura --- */
} TipoItem;

typedef struct {
  TipoItem itens[TAMANHO_MAXIMO];
  TipoApontador primeiro, ultimo;
} TipoLista;

/* ========================================================================== */

void Inicializa(TipoLista *lista){ 
    lista->primeiro = INICIO_ARRANJO;
    lista->ultimo = lista->primeiro;
}  

int Vazia(TipoLista lista){ 
    return (lista.primeiro == lista.ultimo);
}  

void Insere(TipoItem elemento, TipoLista *lista){ 
    if (lista->ultimo == TAMANHO_MAXIMO) 
        printf("Lista Cheia! \n");
    else { 
        lista->itens[lista->ultimo] = elemento;
        lista->ultimo++;      
    }
}

void Retira(TipoApontador posicao, TipoLista *lista, TipoItem *elemento){ 
    int indice;

    if (Vazia(*lista) || posicao > (lista->ultimo-1)){ 
        printf(" Erro! Posicao nao existe \n");
        return;
    }
    *elemento = lista->itens[posicao];
    lista->ultimo--;
    for (indice = posicao; indice < lista->ultimo; indice++)
        lista->itens[indice] = lista->itens[indice+1];
}

void Imprime(TipoLista lista){ 
    int indice;

    for (indice = lista.primeiro; indice < lista.ultimo; indice++)
        printf("%d ", lista.itens[indice].chave);

    printf("\n");
}

/* ========================================================================== */

int main(int argc, char *argv[]){ 
  int i, j, k, n, tamanho;
  int vetor[TAMANHO_MAXIMO];

  TipoLista lista;
  TipoItem item;

  tamanho = 10;

  Inicializa(&lista);
  
  /*Gera uma permutacao aleatoria de chaves entre 1 e maximo*/
  for(i = 0; i < tamanho; i++) 
        vetor[i] = i + 1;

  for(i = 0; i < tamanho; i++){ 
        k =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
        j =  (int) (10.0 * rand()/(RAND_MAX + 1.0));
        n = vetor[k];
        vetor[k] = vetor[j];
        vetor[j] = n;
  }
  
  /*Insere cada chave na lista */
  for (i = 0; i < tamanho; i++){ 
    item.chave = vetor[i];
    Insere(item, &lista);
  }
  Imprime(lista);

  /*Retira cada chave da lista */
  for(i = 0; i < tamanho; i++){ /*escolhe uma chave aleatoriamente */
    j = (int) ((lista.ultimo - 1) * rand() / (RAND_MAX + 1.0));
    /*retira chave apontada */
    Retira(j, &lista, &item);
  }

  Imprime (lista);
  return(0);
}
