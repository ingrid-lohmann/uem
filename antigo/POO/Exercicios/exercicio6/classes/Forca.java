package classes;

public class Forca {

  public String nome;
  public float valor;

  public String getNome() {
    return nome;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

  public float getValor() {
    return valor;
  }

  public void setValor(float valor) {
    this.valor = valor;
  }

  @Override
  public String toString() {
    return "\n Força: {" + '\n' +
        "nome: '" + nome + '\'' + "," + '\n' +
        "valor: " + valor + '\n' +
        "}";
  }
}
