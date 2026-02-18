/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em verificar se a senha digitada pelo usário é correta ou não e, dependendo do resultado liberar ou não o acesso.

2) DEFINIÇÃO DO TIPO DOS DADOS
  O dado utilizado nesse programa é:
    Um do tipo int (int password) que receberá o valor digitado pelo usuário.
  um do tipo int (int authorizedPassword) que contém a senha de acesso que será usada na comparação.

3) CONSTRUÇÃO DO PROGRAMA
  O programa primeiro recebe do usuário o valor da senha, em seguida um bloco de IF será iniciado comparando o valor recibida com o valor da variável authorizedPassword. Caso a comparação se mostre verdadeira, o acesso é liberado, caso contrário o acesso é negado.

4) TESTES
  Casos de testes:
    Acesso permitido:
      password: 1234

    Acesso negado:
      Qualquer valor fornecido que seja diferente de 1234

5) REVISÃO
  Em resumo, o usuário deve fornecer a senha, o programa irá comparar o valor fornecido com o valor contido na variável authorizedPassword, caso sejam iguais o acesso é liberado, caso contrário será negado.
*/


#include <stdio.h>

int main(void) {
  printf("*** PROGRAMA PARA VERIFICAR SENHA DE ACESSO *** \n");

  int password, authorizedPassword;

  authorizedPassword = 1234;

  printf("\nSenha: ");
  scanf("%i", &password);
  
  if (password == authorizedPassword) {
    printf("\nSenha correta!");
    printf("\nAcesso autorizado! Seja bem vindo Givanildo!");
  } else {
    printf("\n\aOps! Senha incorreta!");
    printf("\nAcesso negado!");
  }
  
  return 0;
}

