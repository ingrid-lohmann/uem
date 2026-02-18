// DISCENTE: INGRID LOHMANN 
// RA: 117698

package exercicio4;

import classes.Caneta;

class Main {
  public static void main(String[] args) {
    Caneta caneta1 = new Caneta();

    caneta1.setCarga(3);
    caneta1.setCor("verde");
    caneta1.setMarca("uni-ball");
    caneta1.setEspessura(0.7f);

    System.out.println("Informações da caneta:");
    System.out.println("Cor: " + caneta1.getCor());
    System.out.println("Marca: " + caneta1.getMarca());
    System.out.println("Carga: " + caneta1.getCarga() + "ml");
    System.out.println("Espessura: " + caneta1.getEspessura() + "mm");

  }
}