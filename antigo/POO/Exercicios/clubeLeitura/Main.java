// DISCENTE: INGRID LOHMANN
// RA: 117698

import java.util.Scanner;
import java.time.LocalDate;
import java.time.format.ResolverStyle;
import java.time.format.DateTimeFormatter;

import classes.Amigo;
import classes.Caixa;
import classes.Revista;
import classes.Emprestimo;

public class Main {
  public static void main(String[] args) {
    int TAM;

    LocalDate hoje = LocalDate.now();
    DateTimeFormatter formatoData = DateTimeFormatter.ofPattern("dd/MM/yyyy").withResolverStyle(ResolverStyle.STRICT);
    LocalDate dataDevolucao = hoje.plusDays(7);

    Caixa caixa = new Caixa();
    Amigo amigo = new Amigo();
    Revista revista = new Revista();
    Emprestimo emprestimo = new Emprestimo();

    Scanner dados = new Scanner(System.in);

    System.out.println("*** Informe os dados do amigo ***");
    System.out.print("* Nome: ");
    amigo.setNome(dados.nextLine());
    System.out.print("* Whatsapp: ");
    amigo.setWhatsapp(dados.nextLine());
    System.out.print("* Origem: ");
    amigo.setOrigem(dados.nextLine());
    System.out.print("\n\n");

    System.out.println("*** Informe quantas revistas deseja cadastrar ***");

    TAM = dados.nextInt();

    System.out.println("*** Informe os dados das revistas ***");
    for (int i = 0; i < TAM; i++) {
      System.out.print("* Título: ");
      revista.setTitulo(dados.nextLine());
      dados.nextLine();
      System.out.print("* Coleção: ");
      revista.setColecao(dados.nextLine());
      System.out.print("* Edição: ");
      revista.setEdicao(dados.nextInt());
      dados.nextLine();
      System.out.print("* Ano: ");
      revista.setAno(dados.nextInt());
      dados.nextLine();
      System.out.print("* Número da caixa de armazenamento: ");
      caixa.setNumero(dados.nextInt());
      dados.nextLine();
      System.out.print("* Descrição da caixa de armazenamento: ");
      caixa.setDescricao(dados.nextLine());
      revista.setCaixa(caixa);
      emprestimo.adicionarRevista(revista);
      revista = new Revista();
      System.out.print("\n");
    }

    emprestimo.setAmigo(amigo);
    emprestimo.setDataEmprestimo(hoje.format(formatoData));
    emprestimo.setDataDevolucao(dataDevolucao.format(formatoData));

    dados.close();
    System.out.print("*\n\n");

    System.out.println("*** Conferência dos dados do empréstimo ***");
    System.out.print("\n");
    System.out.print("* Amigo:  ");
    System.out.print("\n");
    System.out.print("- Nome:  ");
    System.out.println(emprestimo.getAmigo().getNome());
    System.out.print("- Whatsapp:  ");
    System.out.println(emprestimo.getAmigo().getWhatsapp());
    System.out.print("- Origem:  ");
    System.out.println(emprestimo.getAmigo().getOrigem());
    System.out.print("\n");
    System.out.print("* Data de empréstimo:  ");
    System.out.println(emprestimo.getDataEmprestimo());
    System.out.print("\n");
    System.out.print("* Data de devolução:  ");
    System.out.println(emprestimo.getDataDevolucao());
    System.out.print("*\n\n");
    System.out.print("* Revistas emprestadas:  ");
    for (int i = 0; i < TAM; i++) {
      System.out.print("\n");
      System.out.print("- Título:  ");
      System.out.println(emprestimo.getRevista(i).getTitulo());
      System.out.print("- Coleção:  ");
      System.out.println(emprestimo.getRevista(i).getColecao());
      System.out.print("- Ano:  ");
      System.out.println(emprestimo.getRevista(i).getAno());
      System.out.print("- Edição:  ");
      System.out.println(emprestimo.getRevista(i).getEdicao());
      System.out.print("- Número da caixa:  ");
      System.out.println(emprestimo.getRevista(i).getCaixa().getNumero());
      System.out.print("- Descrição da caixa:  ");
      System.out.println(emprestimo.getRevista(i).getCaixa().getDescricao());
    }
  }
}