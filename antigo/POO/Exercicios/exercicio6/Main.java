// DISCENTE: INGRID LOHMANN
// RA: 117698

import classes.Forca;
import classes.Habilidade;
import classes.Lado;
import classes.Ordem;
import classes.Personagem;
import classes.SabreLuz;

public class Main {
    public static void main(String[] args) {
        Habilidade habilidadeTelepatia = new Habilidade();
        habilidadeTelepatia.setId(1);
        habilidadeTelepatia.setNomeHabilidade("Telepatia");
        habilidadeTelepatia
                .setDescricao(
                        "Pode manipular os outros mentalmente com a Força para enganar, mutilar ou até mesmo matar.");

        Habilidade habilidadeVaapad = new Habilidade();
        habilidadeVaapad.setId(2);
        habilidadeVaapad.setNomeHabilidade("Vaapad");
        habilidadeVaapad.setDescricao(
                "Pode usar a raiva e a agressão dos outros para se tornar mais forte, mais rápido e se alimentar de seu ódio para amplificar suas estatísticas.");

        Habilidade habilidadePercepcao = new Habilidade();
        habilidadePercepcao.setId(3);
        habilidadePercepcao.setNomeHabilidade("Percepção do Ponto de ruptura");
        habilidadePercepcao.setDescricao(
                "Pode usar a Força para lhe dizer como lidar com os inimigos, quais são suas fraquezas e pontos fortes.");

        Habilidade habilidadeTelecinese = new Habilidade();
        habilidadeTelecinese.setId(4);
        habilidadeTelecinese.setNomeHabilidade("Telecinese");
        habilidadeTelecinese.setDescricao(
                "Pode colocar sua mente literalmente sobre a matéria, capaz de explodir oponentes, se proteger ou desarmar pessoas, seus limites são apenas aqueles da criatividade que o Usuário da Força possui.");

        Habilidade habilidadeTutaminis = new Habilidade();
        habilidadeTutaminis.setId(5);
        habilidadeTutaminis.setNomeHabilidade("Tutaminis");
        habilidadeTutaminis.setDescricao(
                "Pode atrair energia potencialmente prejudicial para seu corpo e difundi-la ou canalizá-la completamente.");

        Lado ladoLuz = new Lado();
        ladoLuz.setId(1);
        ladoLuz.setNome("Lado luz");

        Ordem ordemJedi = new Ordem();
        ordemJedi.setId(1);
        ordemJedi.alterarNomeOrdem("Ordem Jedi");
        ordemJedi.setLado(ladoLuz);

        Personagem maceWindu = new Personagem();

        SabreLuz sabreLuzMaceWindu = new SabreLuz();
        sabreLuzMaceWindu.setCor("Roxo");
        sabreLuzMaceWindu.setCristal("Ametista");

        Forca forcaMaceWindu = new Forca();
        forcaMaceWindu.setNome("Força da Luz");
        forcaMaceWindu.setValor(10000);

        maceWindu.setId(1);
        maceWindu.setOrdem(ordemJedi);
        maceWindu.setNome("Mace Windu");
        maceWindu.setForca(forcaMaceWindu);
        maceWindu.setAposentado(true);
        maceWindu.setSabreLuz(sabreLuzMaceWindu);
        maceWindu.setHabilidades(new Habilidade[] { habilidadeVaapad, habilidadePercepcao, habilidadeTelepatia });

        Personagem mestreYoda = new Personagem();

        SabreLuz sabreLuzMestreYoda = new SabreLuz();
        sabreLuzMestreYoda.setCor("Verde");
        sabreLuzMestreYoda.setCristal("Cristal Kyber");

        Forca forcaMestreYoda = new Forca();
        forcaMestreYoda.setNome("Força da Luz");
        forcaMestreYoda.setValor(10000.99f);

        mestreYoda.setId(0);
        mestreYoda.setOrdem(ordemJedi);
        mestreYoda.setNome("Mestre Yoda");
        mestreYoda.setForca(forcaMestreYoda);
        mestreYoda.setSabreLuz(sabreLuzMestreYoda);
        mestreYoda.setAposentado(true);
        mestreYoda.setHabilidades(new Habilidade[] { habilidadeTelepatia, habilidadeTelecinese, habilidadeTutaminis });

        System.out.println("Jedi 1: " + mestreYoda);
        System.out.println("Jedi 2: " + maceWindu);

        Ordem ordem = new Ordem();

        // ordem.setNomeOrdem("Ordem Jedi"); The method setNomeOrdem(String) from the
        // type Ordem is not visible
        ordem.alterarNomeOrdem("Ordem Sith");

        System.out.println("\nNova ordem: " + ordem.getNomeOrdem());

        // O nome dessa técnica, que impede que outros objetos alterem o nome da ordem
        // diretamente é chamado
        // de encapsulamento. É uma técnica de programação que ajuda a garanti a
        // integridade dos dados.
    }
}
