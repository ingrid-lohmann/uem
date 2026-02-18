// DISCENTE: INGRID LOHMANN 
// RA: 117698

package exercicio3;

import classes.Caneta;

class Main {
  public static void main(String[] args) {
    System.out.println("Instanciando a classe Caneta");
    System.out.println("Instanciando a classe Marca");

    Caneta caneta1 = new Caneta();
    Caneta caneta2 = new Caneta();

    caneta1.carga = 3;
    caneta1.cor = "rosa";
    caneta1.marca.id = 120;
    caneta1.espessura = (float) 0.7;
    caneta1.marca.fornecedor = "uni-ball";
    caneta1.marca.nome = "Signo Sparkling";
    caneta1.marca.endereco.numero = 23;
    caneta1.marca.endereco.pais = "Japão";
    caneta1.marca.endereco.rua = "5 Chome";
    caneta1.marca.endereco.cidade = "Tokyo";
    caneta1.marca.endereco.cep = "140-00011";

    caneta2.carga = 3;
    caneta2.cor = "azul";
    caneta2.marca.id = 93;
    caneta2.espessura = (float) 0.4;
    caneta2.marca.fornecedor = "BIC";
    caneta2.marca.nome = "BIC Intensity";
    caneta2.marca.endereco.numero = 12;
    caneta2.marca.endereco.cep = "192110";
    caneta2.marca.endereco.pais = "França";
    caneta2.marca.endereco.cidade = "Paris";
    caneta2.marca.endereco.rua = "Victor Hugo";

    System.out.println("CANETA 1: " + caneta1);
    System.out.println("CANETA 2: " + caneta2);
  }
}