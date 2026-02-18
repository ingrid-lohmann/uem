// ALUNA: INGRID LOHMANN RA: 1117698
/*
    Exemplos:
      - firstVector = {1, 2, 3, 4, 5, 6, 7}, higherNumber = 7, secondVector =
   {0.14,  0.29,  0.43,  0.57,  0.71,  0.86,  1.00} 
    -firstVector = {10, 7, 9, 17,
   65, 1, 71}, higherNumber = 71, secondVector = {0.14,  0.10,  0.13,  0.24,
   0.92,  0.01,  1.00} 
Entrada: 7 números 
Processamento: comparar os números,
   achar o maior e dividir os valores do primeiro vetor por esse número e gerando um segundo vetor 
Saída: segundo vetor
*/

#include <assert.h>
#include <stdio.h>

void buildVector(float firstVector[7]) {
  int i = 0;
  float secondVector[7] = {}, higherNumber = 0;

  for (i = 0; i < 7; i++) {
    if (firstVector[i] > higherNumber) {
      higherNumber = firstVector[i];
    }
  }

  printf("\nO maior número encontrado foi: %.2f \n", higherNumber);

  for (i = 0; i < 7; i++) {
    secondVector[i] = firstVector[i] / higherNumber;
  }

  printf("\nSegundo vetor: ");
  printf("{");
  for (i = 0; i < 7; i++) {
    printf("%.2f, ", secondVector[i]);
  }
  printf("}");
}

// void testes() {
//   float firstVector[7] = {1,2,3,4,5,6,7};
//   float secondVector[7] = {0.14, 0.29, 0.43, 0.57, 0.71, 0.86,  1.00};
//   for (int i = 0; i < 7; ++i) {
//      assert(buildVector(firstVector[i]) == secondVector[i]);
//   }
//   printf("Testes executados com sucesso! \n\n");
// }

int main(void) {

  float firstVector[7] = {}, secondVector[7] = {};
  int i = 0;

  printf("*** INSTRUÇÃO *** \n");
  printf("Será solicitado a entrada de 7 valores para constituir o vetor. \n");

  for (i = 0; i < 7; i++) {
    printf("\nDigite o %iº valor: ", i + 1);
    scanf("%f", &firstVector[i]);
  }

  buildVector(firstVector);

  return 0;
}