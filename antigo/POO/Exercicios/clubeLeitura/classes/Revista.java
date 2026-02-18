package classes;

public class Revista {
  private Integer ano;
  private String titulo;
  private Caixa caixa;
  private String colecao;
  private Integer edicao;

  public Caixa getCaixa() {
    return caixa;
  }

  public void setCaixa(Caixa caixa) {
    this.caixa = caixa;
  }

  public String getColecao() {
    return colecao;
  }

  public void setColecao(String colecao) {
    this.colecao = colecao;
  }

  public void setEdicao(Integer edicao) {
    this.edicao = edicao;
  }

  public Integer getEdicao() {
    return edicao;
  }

  public Integer getAno() {
    return ano;
  }

  public void setAno(Integer ano) {
    this.ano = ano;
  }

  public void setTitulo(String titulo) {
    this.titulo = titulo;
  }

  public String getTitulo() {
    return titulo;
  }
}
