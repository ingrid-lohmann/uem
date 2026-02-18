// ALUNA: INGRID LOHMANN RA: 1117698
/*
  Exemplos:
    - matrix = {1,2,3,4,5,6,7,8,9,10,11,12}, sum = 78
    - matrix = {11,22,33,44,55,66,77,88,99,1100,1122,1133}, sum = 3850
  Entrada: 12 números
  Processamento: somar os valores dos elementos da matriz
  Saída: valor total da soma
*/

#include <stdio.h>
#include <assert.h>

void displayMatrix(float matrix[4][3])
{
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      printf("%.2f  ", matrix[i][j]);
    }
    printf("\n");
  }
}

float sumValues(float matrix[4][3])
{
  float sum = 0;

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      sum = sum + matrix[i][j];
    }
  }

  return sum;
}

void unitTests()
{
  float fisrtMatrix[4][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
  float secondMatrix[4][3] = {11, 22, 33, 44, 55, 66, 77, 88, 99, 1100, 1122, 1133};
  assert(sumValues(fisrtMatrix) == 78.0);
  assert(sumValues(secondMatrix) == 3850.0);
  printf("Testes executados com sucesso!!\n\n");
}

int main(void)
{
  int i, j;
  float matrix[4][3], sum = 0;

  unitTests();

  printf("*** INSTRUÇÃO *** \n");
  printf("Soma dos elementos da matrix 4x3 \n\n");

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      printf("Digite o elemento [%i] [%i]: ", i + 1, j + 1);
      scanf("%f", &matrix[i][j]);
    }
  }

  printf("\n");

  sum = sumValues(matrix);

  printf("\nMatriz inserida: \n");

  displayMatrix(matrix);

  printf("\nA soma dos elementos é igual a: %.2f \n", sum);

  return 0;
}