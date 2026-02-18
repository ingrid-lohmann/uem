public class Poligono {
  public String cor;
  private Integer altura;
  private Integer largura;

  public void setAltura(Integer altura) {
    this.altura = altura;
  }

  public void setLargura(Integer largura) {
    this.largura = largura;
  }

  public void calcularArea() {
    System.out.println("Area: " + largura*altura);
  }

}



public class Retangulo extends Poligono {
  public Retangulo(Integer altura, Integer largura) {
    super();
    setAltura(altura);
    setLargura(largura);
  }

  public void calcularArea() {
    System.out.println("Area: " + (getAltura() * getLargura()));
  }

}

public class Triangulo extends Poligono {

  private Integer base;
  public Triangulo(Integer altura, Integer base) {
    super();
    setAltura(altura);
    this.base = base;
  }

  public void calcularArea() {
    System.out.println("Area: " + ((base  *getAltura())/2));
  }

}

public class Caneta {
  private String cor;
  private Marca marca;

  public void setCor(String cor) {
    this.cor = cor;
  }

  public void setMarca(Marca marca) {
    this.marca = marca;
  }

  public String getCor() {
    return cor;
  }

  public Marca getMarca() {
    return marca;
  }

}

public class Marca {
  public String nome;
  public String fornecedor;

  public String getFornecedor() {
    return fornecedor;
  }

  public String getNome() {
    return nome;
  }

  public void setFornecedor(String fornecedor) {
    this.fornecedor = fornecedor;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

}



public class Filme {
  private String nome;
  private Integer ano;

  public Integer getAno() {
    return ano;
  }

  public String getNome() {
    return nome;
  }

  public void setAno(Integer ano) {
    this.ano = ano;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }
}

public class CanalStreaming {
  private Integer numero;
  private String nome;
  private ArrayList<Filme> filmes = new ArrayList<>();

  public void setNome(String nome) {
    this.nome = nome;
  }

  public void setNumero(Integer numero) {
    this.numero = numero;
  }

  public String getNome() {
    return nome;
  }

  public Integer getNumero() {
    return numero;
  }

  public void adicionarFilme(Filme filme) {
    filmes.add(filme);
  }

  public Filme getRevista(int index) {
    return filmes.get(index);
  }

  public void removerRevista(int index) {
    filmes.remove(index);
  }

  public int getQuantidadeRevistas() {
    return filmes.size();
  }

  public ArrayList<Filme> getRevistas() {
    return filmes;
  }

}
