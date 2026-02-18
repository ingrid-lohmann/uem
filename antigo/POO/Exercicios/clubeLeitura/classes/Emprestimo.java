package classes;

import java.util.ArrayList;
import java.util.Arrays;

public class Emprestimo {
  private Amigo amigo;
  private String dataEmprestimo;
  private String dataDevolucao;
  private ArrayList<Revista> revistas = new ArrayList<>();

  public Amigo getAmigo() {
    return amigo;
  }

  public void setAmigo(Amigo amigo) {
    this.amigo = amigo;
  }

  public String getDataDevolucao() {
    return dataDevolucao;
  }

  public void setDataDevolucao(String dataDevolucao) {
    this.dataDevolucao = dataDevolucao;
  }

  public String getDataEmprestimo() {
    return dataEmprestimo;
  }

  public void setDataEmprestimo(String dataEmprestimo) {
    this.dataEmprestimo = dataEmprestimo;
  }

  public void adicionarRevista(Revista revista) {
    revistas.add(revista);
  }

  public Revista getRevista(int index) {
    return revistas.get(index);
  }

  public void removerRevista(int index) {
    revistas.remove(index);
  }

  public int getQuantidadeRevistas() {
    return revistas.size();
  }

  public ArrayList<Revista> getRevistas() {
    return revistas;
  }
}
