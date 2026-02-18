package entregues.exercicio5.classes;

import java.util.Arrays;

public class Personagem {
  public int id;
  public Ordem ordem;
  public String nome;
  public Forca forca;
  public SabreLuz sabreLuz;
  public boolean aposentado;
  private Habilidade[] habilidades;

  public SabreLuz getSabreLuz() {
    return sabreLuz;
  }

  public Forca getForca() {
    return forca;
  }

  public boolean getAposentado() {
    return aposentado;
  }

  public Habilidade[] getHabilidades() {
    return habilidades;
  }

  public int getId() {
    return id;
  }

  public String getNome() {
    return nome;
  }

  public Ordem getOrdem() {
    return ordem;
  }

  public void setAposentado(boolean aposentado) {
    this.aposentado = aposentado;
  }

  public void setSabreLuz(SabreLuz sabreLuz) {
    this.sabreLuz = sabreLuz;
  }

  public void setHabilidades(Habilidade[] habilidades) {
    this.habilidades = habilidades;
  }

  public void setId(int id) {
    this.id = id;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

  public void setOrdem(Ordem ordem) {
    this.ordem = ordem;
  }

  public void setForca(Forca forca) {
    this.forca = forca;
  }
}
