package classes;

public class Pessoa {
  public Double peso;
  public String nome;
  public Double altura;
  public Integer idade;

  public Double getPeso() {
    return peso;
  }

  public void setPeso(Double peso) {
    this.peso = peso;
  }

  public String getNome() {
    return nome;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

  public Double getAltura() {
    return altura;
  }

  public void setAltura(Double altura) {
    this.altura = altura;
  }

  public Integer getIdade() {
    return idade;
  }

  public void setIdade(Integer idade) {
    this.idade = idade;
  }

  public void engordar(int quilos) {
    peso += quilos;
  }

  public void emagrecer(int quilos) {
    peso -= quilos;
  }

  public void envelhecer() {
    idade++;

    if (idade < 21) {
      altura += 0.5;
    }
  }
}