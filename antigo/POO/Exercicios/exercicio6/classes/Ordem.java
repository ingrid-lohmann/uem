package classes;

public class Ordem {
  public int id;
  private String nomeOrdem;

  public Lado lado = new Lado();

  public int getId() {
    return id;
  }

  public Lado getLado() {
    return lado;
  }

  public String getNomeOrdem() {
    return nomeOrdem;
  }

  public void setId(int id) {
    this.id = id;
  }

  public void setLado(Lado lado) {
    this.lado = lado;
  }

  // Método set do nome da ordem passado para privado
  private void setNomeOrdem(String nomeOrdem) {
    this.nomeOrdem = nomeOrdem;
  }

  // Método público para alterar o nome da ordem
  public void alterarNomeOrdem(String novoNome) {
    this.setNomeOrdem(novoNome);
  }

  @Override
  public String toString() {
    return "\n Ordem: {" + '\n' +
        "id: '" + id + '\'' + "," + '\n' +
        "nome: '" + nomeOrdem + '\'' + "," + '\n' +
        "lado: " + lado + '\n' +
        "}";
  }
}