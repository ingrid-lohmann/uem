package classes;

public class Marca {
  public int id;
  public String nome;
  public String fornecedor;

  public Endereco endereco = new Endereco();

  @Override
  public String toString() {
    return "{" + "\n" +
        "\t\tid: " + id + "," + "\n" +
        "\t\tnome: '" + nome + '\'' + "," + "\n" +
        "\t\tfornecedor: '" + fornecedor + '\'' + "," + "\n" +
        "\t\tendereço: " + endereco + "\n" +
        "\t\t}" + "," + "\n";
  }
}