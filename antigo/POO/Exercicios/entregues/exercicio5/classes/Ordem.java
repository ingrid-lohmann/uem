package entregues.exercicio5.classes;

public class Ordem {
  public int id;
  public Lado lado;
  public String NomeOrdem;

  public int getId() {
    return id;
  }

  public Lado getLado() {
    return lado;
  }

  public String getNomeOrdem() {
    return NomeOrdem;
  }

  public void setId(int id) {
    this.id = id;
  }

  public void setLado(Lado lado) {
    this.lado = lado;
  }

  public void setNomeOrdem(String nomeOrdem) {
    NomeOrdem = nomeOrdem;
  }
}
