#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int LED;
int contaLED;

void executarOperacoes(char *argv)
{
    FILE *arquivo, *saida, *operacoes, *espacosDisponiveis;

    int achou;
    char *campo;
    short tamanho;
    char *comando[2];
    char buffer[256];
    char bufferOperacoes[256];

    operacoes = fopen(argv, "r");

    if (operacoes == NULL)
    {
        printf("Erro na importação do arquivo de operações %s!", argv);
        exit(EXIT_FAILURE);
    }

    arquivo = fopen("dados.dat", "r+b");

    fread(&LED, sizeof(LED), 1, arquivo);

    saida = fopen("saida.txt", "w");

    espacosDisponiveis = fopen("espacosDisponiveis.txt", "w");

    while (fgets(bufferOperacoes, sizeof(bufferOperacoes), operacoes) != NULL)
    {
        fseek(arquivo, 0, SEEK_SET);
        fread(&LED, sizeof(LED), 1, arquivo);

        achou = 0;

        comando[0] = strtok(bufferOperacoes, " ");

        comando[1] = strtok(NULL, "\n");

        if (strcmp(comando[0], "b") == 0)
        {
            printf("\nBusca pelo registro de chave \'%s\'", comando[1]);

            fread(&tamanho, sizeof(tamanho), 1, arquivo);
            fread(buffer, sizeof(char), tamanho, arquivo);

            while (!achou && !feof(arquivo))
            {

                campo = strtok(buffer, "|");

                if (strcmp(campo, comando[1]) == 0)
                {
                    achou = 1;
                }
                else
                {
                    fread(&tamanho, sizeof(tamanho), 1, arquivo);
                    fread(buffer, sizeof(char), tamanho, arquivo);
                }
            }

            if (achou != 0)
            {
                int cont = 1;

                printf("\n%s|", campo);

                campo = strtok(NULL, "|");

                while (cont < 6)
                {
                    printf("%s|", campo);
                    campo = strtok(NULL, "|");
                    cont++;
                }
                printf("  (Tamanho = %d bytes)\n", tamanho);
            }
            else
                printf("\nOps! Registro de id %s não encontrado!\n", comando[1]);
        }
        else if (strcmp(comando[0], "i") == 0)
        {
            char aux;
            int LEDAtual;
            int LEDProximo;
            int LEDAnterior = -1;
            int LEDAuxiliar = LED;
            short tamanhoAuxiliar;

            if (LEDAuxiliar == -1)
            {
                strcpy(buffer, comando[1]);

                tamanho = strlen(buffer);

                fseek(arquivo, 0, SEEK_END);

                fwrite(&tamanho, sizeof(tamanho), 1, arquivo);

                fwrite(buffer, sizeof(char), tamanho, arquivo);

                campo = strtok(buffer, "|");

                printf("\nInserção do registro de chave \'%s\'. (%d bytes)\n", campo, tamanho);

                printf("Local: fim do arquivo\n");
            }
            else
            {
                int inserido = 0;
                strcpy(buffer, comando[1]);
                tamanho = strlen(buffer);
                while (LEDAuxiliar != -1 && inserido == 0)
                {
                    LEDAtual = LEDAuxiliar;

                    fseek(arquivo, LEDAtual, SEEK_SET);

                    fread(&tamanhoAuxiliar, sizeof(tamanhoAuxiliar), 1, arquivo);

                    fgetc(arquivo);

                    fread(&LEDProximo, sizeof(LEDProximo), 1, arquivo);
                    if (tamanho < tamanhoAuxiliar && LEDAnterior == -1)
                    {
                        fseek(arquivo, LEDAtual + sizeof(tamanho), SEEK_SET);

                        fwrite(buffer, sizeof(char), tamanho, arquivo);

                        fseek(arquivo, 0, SEEK_SET);

                        fwrite(&LEDProximo, sizeof(LEDProximo), 1, arquivo);

                        campo = strtok(buffer, "|");

                        printf("\nInserção do registro chave \'%s\'. (%d bytes)\n", campo, tamanho);

                        printf("Tamanho do espaço reutilizado: %d bytes (Sobra de %d bytes) \n", tamanhoAuxiliar, tamanhoAuxiliar - tamanho - 2);

                        printf("Local: offset = %d bytes (0x%x)\n", LEDAtual, LEDAtual);

                        inserido = 1;
                    }
                    else if (tamanho < tamanhoAuxiliar && LEDAnterior != -1)
                    {
                        fseek(arquivo, LEDAtual + sizeof(tamanho), SEEK_SET);

                        fwrite(buffer, sizeof(char), tamanho, arquivo);

                        fseek(arquivo, LEDAnterior + sizeof(tamanho) + sizeof(char), SEEK_SET);

                        fwrite(&LEDProximo, sizeof(LEDProximo), 1, arquivo);

                        campo = strtok(buffer, "|");

                        printf("\nInserção do registro de chave \'%s\'. (%d bytes)\n", campo, tamanho);
                        printf("Tamanho do espaco reutilizado: %d bytes (Sobra de %d bytes)\n", tamanhoAuxiliar, tamanhoAuxiliar - tamanho - 2);
                        printf("Local: offset = %d bytes (0x%x)\n", LEDAtual, LEDAtual);

                        inserido = 1;
                    }
                    else if (tamanho > tamanhoAuxiliar)
                    {
                        LEDAnterior = LEDAtual;
                        LEDAuxiliar = LEDProximo;
                    }
                }
                if (LEDAuxiliar == -1)
                {
                    fseek(arquivo, 0, SEEK_END);

                    fwrite(&tamanho, sizeof(tamanho), 1, arquivo);

                    fwrite(buffer, sizeof(char), tamanho, arquivo);

                    campo = strtok(buffer, "|");

                    printf("\nInserção do registro de chave \'%s\'. (%d bytes)\n", campo, tamanho);
                    printf("Local: fim do arquivo\n");

                    inserido = 1;
                }
            }
        }
        else if (strcmp(comando[0], "r") == 0)
        {
            printf("\nRemoção do registro de chave \'%s\'", comando[1]);

            fread(&tamanho, sizeof(tamanho), 1, arquivo);

            fread(buffer, sizeof(char), tamanho, arquivo);

            while (!achou && !feof(arquivo))
            {
                campo = strtok(buffer, "|");

                if (strcmp(campo, comando[1]) == 0)
                {
                    achou = 1;
                }
                else
                {
                    fread(&tamanho, sizeof(tamanho), 1, arquivo);
                    fread(buffer, sizeof(char), tamanho, arquivo);
                }
            }
            if (achou != 0)
            {
                int tamanhoLEDInicio;

                char caractereRemovedor = '*';

                fseek(arquivo, ftell(arquivo) - tamanho, SEEK_SET);

                tamanhoLEDInicio = ftell(arquivo) - sizeof(tamanho); // retorna começo do arq

                fwrite(&caractereRemovedor, sizeof(caractereRemovedor), 1, arquivo); // add * depois do tamanho

                fwrite(&LED, sizeof(LED), 1, arquivo);

                printf("\nRegistro de id %s removido! Tamanho total de %d bytes", comando[1], tamanho);

                LED = tamanhoLEDInicio;

                printf("\nLocal: offset %d bytes    (0x%x)\n", LED, LED);

                fprintf(saida, "%i;%i\n", LED, tamanho);

                contaLED++;
            }
            else
                printf("\nOps! Registro de id %s não encontrado!\n", comando[1]);

            fseek(arquivo, 0, SEEK_SET);           // retorna o ponteiro para o começo do arquivo
            fwrite(&LED, sizeof(LED), 1, arquivo); // escreve a led no arquivo e move o ponteiro
        }
        fseek(arquivo, sizeof(LED), SEEK_SET); // coloca o ponteiro na posição 4
    }
    fprintf(espacosDisponiveis, "%i\n", contaLED);

    fclose(saida);
    fclose(arquivo);
    fclose(operacoes);
    fclose(espacosDisponiveis);
}

void imprimirLed()
{
    FILE *arquivo, *espacosDisponiveis;
    char str[100];

    arquivo = fopen("saida.txt", "r");
    espacosDisponiveis = fopen("espacosDisponiveis.txt", "r");

    if (arquivo == NULL || espacosDisponiveis == NULL)
    {
        printf("Ops! Erro ao abrir o arquivo!\n");
        exit(EXIT_FAILURE);
    }

    printf("\nLED -> ");

    char ch;
    while (fgets(str, 100, arquivo) != NULL)
    {
        printf("[");
        printf("offset: %s ", strtok(str, ";"));
        printf("tamamnho: %s ", strtok(NULL, "\n"));
        printf("] -> ");
    }

    while (fgets(str, 100, espacosDisponiveis) != NULL)
    {
        printf("\nTotal: %s espaços disponíveis", strtok(str, "\n"));
    }

    fclose(arquivo);
}

int main(int argc, char *argv[])
{
    if (argc == 3 && strcmp(argv[1], "-e") == 0)
    {
        printf("Execução de operações ativo...Arquivo = %s\n", argv[2]);
        executarOperacoes(argv[2]);
    }
    else if (argc == 2 && strcmp(argv[1], "-p") == 0)
    {
        printf("Imprimindo a LED...Pro favor aguarde.\n");
        imprimirLed();
    }
    else
    {
        fprintf(stderr, "Argumentos incorretos!\n");
        fprintf(stderr, "Modo de uso:\n");
        fprintf(stderr, "$ %s (-i|-e) nome_arquivo\n", argv[0]);
        fprintf(stderr, "$ %s -p\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    return 0;
}