// ALUNA: INGRID LOHMANN RA: 117698
/*
  Exemplos:
    Produto1 -> nome: arroz, cod: 123, preço: 10,
    Produto2 -> nome: pão, cod: 223, preço: 20,
    Produto3 -> nome: macarrão, cod: 345, preço: 5,
    Produto4 -> nome: salsicha, cod: 5456, preço: 25,
    Produto5 -> nome: abacaxi, cod: 654, preço: 33,
    Produto6 -> nome: melão, cod: 633, preço: 89,
    Produto7 -> nome: feijão, cod: 8768, preço: 11,
    Produto8 -> nome: alface, cod: 3242, preço: 32,
    Produto9 -> nome: peixe, cod: 54645, preço: 27,
    Produto10 -> nome: bolacha, cod: 43, preço: 112,
    Média: -> 36,4

  Entrada: nome e codigo e preço de 10 produtos
  Processamento: passa o valor da struct para uma função de produto e depois
  retornar a média dos valores;
*/

#include <stdio.h>
#include <string.h>

typedef struct Produto {
  char nome[100];
  int cod;
  float preco;
} Produto;

void imprimirProduto(Produto p) {
  printf("\nProduto: %s", p.nome);
  printf("\nCódigo: %i", p.cod);
  printf("\nPreço: %.2f", p.preco);
}

int mediaPrecos(Produto p) {
  float media = 0;
  media = media + p.preco;
  return media;
}

Produto cadastrarProduto() {
  Produto p;
  printf("\nDigite o produto: ");
  scanf("%s", p.nome);
  printf("Digite código: ");
  scanf("%i", &p.cod);
  printf("Digite o preço: ");
  scanf("%f", &p.preco);

  return p;
}

int main() {

  printf("*** CADASTRO DE PRODUTOS *** \n");

  printf("\n");

  int i;
  float media = 0;
  Produto produtos[10];

  for (i = 0; i < 10; i++) {
    printf("\n%iº produto: ", i + 1);
    produtos[i] = cadastrarProduto();
  }

  for (i = 0; i < 10; i++) {
    media = mediaPrecos(produtos[i]) / 10;
  }

printf("\n");

  printf("Média: %.2f", media);

  return 0;
}