// ALUNA: INGRID LOHMANN RA: 117698
/*
  Exemplos:
    Aluno1 -> RA:123, nome: zelda -> Nome: zelda RA: 123
    Aluno2 -> RA:456, nome: meg -> Nome: meg RA: 456
    Aluno3 -> RA:333, nome: panda -> Nome: panda RA: 333

  Entrada: nome e ra de um aluno
    Processamento: passa o valor da struct para uma função de cadastro e depois imprimir o que foi digitado utilizando essa mesma função;
*/

#include <stdio.h>
#include <string.h>

struct cadastro {
  char nome[10];
  int ra;
} cadastro;

void cadastrar(struct cadastro c) {

  printf("Digite o nome do aluno: ");
  scanf("%s", c.nome);
  printf("Digite o RA do aluno: ");
  scanf("%i", &c.ra);

  printf("Nome: %s", c.nome);
  printf("\nRA:%i\n", c.ra);
}

int main() {

  printf("*** CADASTRO DE ALUNO *** \n");

  printf("\n");

  struct cadastro aluno;

  cadastrar(aluno);

  return 0;
}