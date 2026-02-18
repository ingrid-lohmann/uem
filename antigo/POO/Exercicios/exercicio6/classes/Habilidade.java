package classes;

public class Habilidade {

  public int id;
  public String descricao;
  public String nomeHabilidade;

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }

  public String getDescricao() {
    return descricao;
  }

  public void setDescricao(String descricao) {
    this.descricao = descricao;
  }

  public String getNomeHabilidade() {
    return nomeHabilidade;
  }

  public void setNomeHabilidade(String nomeHabilidade) {
    this.nomeHabilidade = nomeHabilidade;
  }

  @Override
  public String toString() {
    return "\n Habilidade: {" + '\n' +
        "id: '" + id + '\'' + "," + '\n' +
        "nome: '" + nomeHabilidade + '\'' + "," + '\n' +
        "descrição: " + descricao + '\n' +
        "}";
  }

}
