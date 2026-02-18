package entregues.exercicio5.classes;

public class Habilidade {
  public int id;
  public String descricao;
  public String nomeHabilidade;

  public String getDescricao() {
    return descricao;
  }

  public int getId() {
    return id;
  }

  public String getNomeHabilidade() {
    return nomeHabilidade;
  }

  public void setDescricao(String descricao) {
    this.descricao = descricao;
  }

  public void setId(int id) {
    this.id = id;
  }

  public void setNomeHabilidade(String nomeHabilidade) {
    this.nomeHabilidade = nomeHabilidade;
  }
}
