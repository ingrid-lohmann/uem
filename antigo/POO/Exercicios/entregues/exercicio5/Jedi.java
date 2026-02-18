// DISCENTE: INGRID LOHMANN 
// RA: 117698

package entregues.exercicio5;

import entregues.exercicio5.classes.*;

public class Jedi {
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
        ordemJedi.setNomeOrdem("Ordem Jedi");
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

        String numeroFloatParaString = Float.toString(mestreYoda.getForca().getValor());
        System.out.println("Float -> String" + numeroFloatParaString); // Aqui não é perdido nenhum valor.

        int booleanParaInt = maceWindu.getAposentado() ? 1 : 0;
        System.out.println("Float -> String" + booleanParaInt); // Aqui ocorre uma conversão explícita.
        // Java não permite a conversão implícita de tipos booleanos em inteiros.

        // Conversão implícita
        // Ocorre automaticamente pelo compilador, sem a necessidade de nenhuma ação do
        // programador.
        // Não há perda de informação nessa conversão.
        // Ex:
        float numeroFloat = mestreYoda.getId();
        System.out.println("Conversão implícita de int para float: " + numeroFloat);

        // Conversão explícita
        // Ocorre quando o programador especifica a conversão de uma variável de um tipo
        // para outro.
        // Isso é necessário quando há perda de informação na conversão.
        // Exemplo;
        int piInteiro = (int) mestreYoda.getForca().getValor();
        System.out.println("Conversão explícita de float para int: " + piInteiro);
    }
}
