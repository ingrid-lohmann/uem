package classes;

public class SabreLuz {

  public String cor;
  public String cristal;

  public String getCor() {
    return cor;
  }

  public void setCor(String cor) {
    this.cor = cor;
  }

  public String getCristal() {
    return cristal;
  }

  public void setCristal(String cristal) {
    this.cristal = cristal;
  }

  @Override
  public String toString() {
    return "\n Sabre de luz: {" + '\n' +
        "cor: '" + cor + '\'' + "," + '\n' +
        "cristal: " + cristal + '\n' +
        "}";
  }

}
