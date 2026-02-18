// ALUNA: INGRID LOHMANN RA: 1117698
/*
    Exemplos:
      - firstVector = {1,2,3,4,5}, secondVector =
   {1,2,3,4,5,6}, resultado {1,2,3,4,5}
     - firstVector = {10,14,7,5,3}, secondVector =
   {100,66,47,12,10,8,11}, resultado {10}
Entrada: 5 números e 7 números
Processamento: comparar os números, achar os valores iguais e mostrá-los na tela
Saída: vetor com os valores repetidos
*/

#include <stdio.h>

void commumValues(int firstVector[5], int secondVector[7]) {
  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 7; j++) {
      if (firstVector[i] == secondVector[j]) {
        printf("%i, ", secondVector[j]);
      }
    }
  }
}

int main(void) {

  int firstVector[5], secondVector[7], i, j;

  printf("*** INSTRUÇÃO *** \n");
  printf("Será solicitado a entrada de 5 valores para constituir o primeiro "
         "vetor e depois mais 7 para construir o outro. \n");

  printf("\n");

  for (i = 0; i < 5; i++) {
    printf("\n Digite o %iº valor do vetor A: ", i + 1);
    scanf("%i", &firstVector[i]);
  }

  printf("\n");

  for (i = 0; i < 7; i++) {
    printf("\n Digite o %iº valor vetor B: ", i + 1);
    scanf("%i", &secondVector[i]);
  }

  printf("\n");
  printf("Os valores comuns são:\n");

  commumValues(firstVector, secondVector);
  return 0;
}