package classes;

public class Caneta {
  public String cor;
  public float carga;
  public float espessura;

  public Marca marca = new Marca();

  @Override
  public String toString() {
    return "\nCaneta: {" + '\n' +
        "\tcor: '" + cor + '\'' + "," + '\n' +
        "\tcarga: " + carga + "ml," + '\n' +
        "\tespessura: " + espessura + "mm," + '\n' +
        "\tmarca: " + marca +
        "\t}";
  }
}