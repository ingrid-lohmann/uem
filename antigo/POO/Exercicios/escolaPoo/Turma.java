package Exercicios.escolaPoo;

public class Turma {
  private Integer id;
  private String nome;
  private Professor professor;
  private Aluno[] aluno = new Aluno[3];

  // public Turma() {
  // aluno = new Aluno[3];
  // }

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

  public Professor getProfessor() {
    return professor;
  }

  public Aluno getAluno(Integer pos) {
    return aluno[pos];
  }

  public void setAluno(Aluno aluno, Integer pos) {
    this.aluno[pos] = aluno;
  }

  public void setProfessor(Professor professor) {
    this.professor = professor;
  }
}