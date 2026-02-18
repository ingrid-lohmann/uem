package classes;

public class Endereco {
  public String rua;
  public int numero;
  public String cep;
  public String pais;
  public String cidade;

  @Override
  public String toString() {
    return "{" + "\n" +
        "\t\t\trua: '" + rua + '\'' + "," + "\n" +
        "\t\t\tnúmero: " + numero + "," + "\n" +
        "\t\t\tcep: '" + cep + '\'' + "," + "\n" +
        "\t\t\tcidade: '" + cidade + '\'' + "," + "\n" +
        "\t\t\tpaís: '" + pais + '\'' + "," + "\n" +
        "\t\t\t}" + ",";
  }
}
