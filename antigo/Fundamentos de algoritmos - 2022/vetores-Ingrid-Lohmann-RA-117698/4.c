// ALUNA: INGRID LOHMANN RA: 1117698
/*
  Exemplos:
    - matrix = {1,2,3,4,5,6,7,8,9}, higherNumber = 9, div = {0.11,0.22,0.33,0.44,0.56,0.67,0.78,0.89,1.00}
  - matrix = {2,2,2,2,2,2,2,2,10}, higherNumber = 10, div = {0.22,0.22,0.22,0.22,0.22,0.22,0.22,0.22,1.00}
  - matrix = {22,1,3,5,4,7,8,9,3}, higherNumber = 10, div = {1,0.05,0.14,0.23,0.18,0.32,0.36,0.41,0.14}
  Entrada: 9 números
  Processamento: achar o maior número e dividir os elementos por esse valor
  Saída: matriz divida pelo maior valor da diagonal;
*/

#include <stdio.h>
#include <assert.h>

void displayMatrix(float matrix[3][3])
{
  for (int i = 0; i < 3; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      printf("%.2f  ", matrix[i][j]);
    }
    printf("\n");
  }
}

float findHigherNumber(float matrix[3][3])
{
  float higherNumber = 0;

  for (int i = 0; i < 3; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      if (matrix[i][i] > higherNumber)
      {
        higherNumber = matrix[i][i];
      }
    }
  }

  return higherNumber;
}

void divideMatrix(float matrix[3][3], float higherNumber)
{
  float div[3][3];

  for (int i = 0; i < 3; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      div[i][j] = ((float)matrix[i][j]) / (float)higherNumber;
    }
  }

  printf("\nMatriz final cujo elementos foram divididos por %.2f: \n\n", higherNumber);

  displayMatrix(div);
}

void unitTests()
{
  float fisrtMatrix[4][3] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
  float secondMatrix[4][3] = {11, 22, 33, 44, 99, 66, 77, 88, 55};
  assert(findHigherNumber(fisrtMatrix) == 9);
  assert(findHigherNumber(secondMatrix) == 99);
  printf("Testes executados com sucesso!!\n\n");
}

int main(void)
{
  int i, j;
  float matrix[3][3], div[3][3], higherNumber = 0;

  unitTests();

  printf("*** INSTRUÇÃO *** \n");
  printf("Maior elemento diagonal \n\n");

  for (i = 0; i < 3; i++)
  {
    for (j = 0; j < 3; j++)
    {
      printf("Digite o elemento [%i][%i]: ", i + 1, j + 1);
      scanf("%f", &matrix[i][j]);
    }
  }

  printf("\nMatriz inserida: \n");

  displayMatrix(matrix);

  higherNumber = findHigherNumber(matrix);

  printf("\nO maior elemento da diagonal é: %.2f \n\n", higherNumber);

  divideMatrix(matrix, higherNumber);

  return 0;
}