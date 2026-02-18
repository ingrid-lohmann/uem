package Exercicios.escolaPoo;

import java.util.Scanner;

public class Principal {

  public static void main(String[] args) {
    int TAM = 3;
    Aluno aluno = new Aluno();
    Turma turma = new Turma();
    Professor professor = new Professor();

    Scanner dados = new Scanner(System.in);

    System.out.println("*** Informe o Professor ****");
    System.out.print("* Matrícula:  ");
    professor.setMatricula(dados.nextInt());
    dados.nextLine();
    System.out.print("* Nome:  ");
    professor.setNome(dados.nextLine());
    System.out.print("*\n\n");

    System.out.println("*** Agora informe a turma do Aluno ****");
    System.out.print("* ID:  ");
    turma.setId(dados.nextInt());
    dados.nextLine();
    System.out.print("* Nome:  ");
    turma.setNome(dados.nextLine());

    for (int i = 0; i < TAM; i++) {
      System.out.println("*** Informe o Aluno ****");
      System.out.print("* RA:  ");
      aluno.setRa(dados.nextInt());
      dados.nextLine();
      System.out.print("* Nome:  ");
      aluno.setNome(dados.nextLine());
      turma.setAluno(aluno, i);
      aluno = new Aluno();
    }

    turma.setProfessor(professor);
    dados.close();
    System.out.print("*\n\n");

    System.out.println("*** Relatorio Turma e Aluno ****");
    System.out.print("Id Turma: " + turma.getId() +
        " - Nome Turma: " + turma.getNome() +
        " - Professor: " + turma.getProfessor().getNome());
    System.out.print("*\n\n");

    for (int i = 0; i < TAM; i++) {
      System.out.println("RA:  " + turma.getAluno(i).getRa() +
          " - Aluno: " + turma.getAluno(i).getNome());

    }
    System.out.println("*** Fim Relatorio Turma e Aluno ****");

  }
}