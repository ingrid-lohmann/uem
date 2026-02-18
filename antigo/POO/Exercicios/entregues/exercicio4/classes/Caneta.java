package classes;

public class Caneta {
  public String cor;
  public int carga;
  public String marca;
  public float espessura;

  public int getCarga() {
    return carga;
  }

  public String getCor() {
    return cor;
  }

  public float getEspessura() {
    return espessura;
  }

  public String getMarca() {
    return marca;
  }

  public void setCarga(int carga) {
    this.carga = carga;
  }

  public void setCor(String cor) {
    this.cor = cor;
  }

  public void setEspessura(float espessura) {
    this.espessura = espessura;
  }

  public void setMarca(String marca) {
    this.marca = marca;
  }
}