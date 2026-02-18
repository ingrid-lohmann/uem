// DISCENTE: INGRID LOHMANN
// RA: 117698

import java.util.Scanner;

import classes.Pessoa;

public class Main {
  public static void main(String[] args) {
    Pessoa pessoa = new Pessoa();

    Scanner dados = new Scanner(System.in);

    pessoa.setIdade(14);
    pessoa.setPeso(60.0);
    pessoa.setAltura(173.0);
    pessoa.setNome("Hyoga de Cisne");

    System.out.println("*** Dados: ***");
    System.out.println("Nome: " + pessoa.getNome());
    System.out.println("Idade: " + pessoa.getIdade() + " anos");
    System.out.println("Peso: " + pessoa.getPeso() + " Kg");
    System.out.println("Altura: " + (pessoa.getAltura() / 100) + " m");

    System.out.println("\n");

    System.out.print("Quantos quilos o " + pessoa.getNome() + " deve engordar? ");
    int quilos = dados.nextInt();

    dados.nextLine();

    pessoa.engordar(quilos);

    System.out.println("\n");
    System.out.println("O novo peso de " + pessoa.getNome() + " após a dieta para engordar: ");
    System.out.println("Nome: " + pessoa.getNome());
    System.out.println("Peso: " + pessoa.getPeso() + " Kg");
    System.out.println("\n");

    System.out.print("Quantos quilos o " + pessoa.getNome() + " deve emagrecer? ");
    quilos = dados.nextInt();

    System.out.println("\n");
    System.out.println("O novo peso de " + pessoa.getNome() + "após a dieta de emagrecimento: ");
    System.out.println("Nome: " + pessoa.getNome());
    System.out.println("Peso: " + pessoa.getPeso() + " Kg");
    System.out.println("\n");

    pessoa.envelhecer();

    System.out.println("Parece que " + pessoa.getNome() + " fez aniversário! E sua altura aumentou um pouco: ");

    System.out.println("Nome: " + pessoa.getNome());
    System.out.println("Idade: " + pessoa.getIdade() + " anos");
    System.out.println("Altura: " + (pessoa.getAltura() / 100) + " m");
  }
}
