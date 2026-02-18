package classes;

public class Lado {
  public int id;
  public String nome;

  public void setId(int id) {
    this.id = id;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

  public int getId() {
    return id;
  }

  public String getNome() {
    return nome;
  }

  @Override
  public String toString() {
    return "\n Lado: {" + '\n' +
        "id: '" + id + '\'' + "," + '\n' +
        "nome: '" + nome + '\'' + "," + '\n' +
        "}";
  }

}