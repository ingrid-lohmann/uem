package classes;

import java.util.ArrayList;

public class Turma {
  private Integer id;
  private String nome;
  private Professor professor;
  private ArrayList<Aluno> alunos = new ArrayList<>();

  public Integer getId() {
    return id;
  }

  public void setId(Integer id) {
    this.id = id;
  }

  public String getNome() {
    return nome;
  }

  public void setNome(String nome) {
    this.nome = nome;
  }

  public void setProfessor(Professor professor) {
    this.professor = professor;
  }

  public Professor getProfessor() {
    return professor;
  }

  public void adicionarAluno(Aluno aluno) {
    alunos.add(aluno);
  }

  public Aluno getAluno(int index) {
    return alunos.get(index);
  }

  public void removerAluno(int index) {
    alunos.remove(index);
  }

  public int getQuantidadeAlunos() {
    return alunos.size();
  }

}
