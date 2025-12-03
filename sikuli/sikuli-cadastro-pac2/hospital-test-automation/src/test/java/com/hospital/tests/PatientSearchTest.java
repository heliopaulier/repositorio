package com.hospital.tests;

import org.junit.Test;

public class PatientSearchTest extends BaseSikuliTest {

    @Test
    public void testPatientSearch() {
        System.out.println("Iniciando teste de busca de paciente...");

        // Gerar um nome fake para buscar
        String nomeBusca = FakeDataGenerator.generateFakeName();

        System.out.println("Simulando busca pelo paciente: " + nomeBusca);

        try {
            // Exemplo: Clicar no botão 'Buscar Paciente'
            // clickImage("images/btn_buscar_paciente.png");
            System.out.println("Simulando clique em 'Buscar Paciente'.");
            Thread.sleep(1000);

            // Exemplo: Digitar o nome no campo de busca
            // typeText("images/campo_busca_nome.png", nomeBusca);
            System.out.println("Simulando digitação do nome \"" + nomeBusca + "\" no campo de busca.");
            Thread.sleep(500);

            // Exemplo: Clicar no botão 'Pesquisar'
            // clickImage("images/btn_pesquisar.png");
            System.out.println("Simulando clique em 'Pesquisar'.");
            Thread.sleep(2000);

            // Exemplo: Validar se o paciente foi encontrado (simulado)
            // if (existsImage("images/resultado_busca_nome.png")) {
            //     System.out.println("Paciente \"" + nomeBusca + "\" encontrado com sucesso!");
            // } else {
            //     System.err.println("Erro: Paciente \"" + nomeBusca + "\" não encontrado.");
            //     // throw new FindFailed("Paciente não encontrado.");
            // }
            System.out.println("Simulando validação de resultado de busca: Paciente \"" + nomeBusca + "\" encontrado.");

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Teste interrompido: " + e.getMessage());
            throw new RuntimeException(e);
        }

        System.out.println("Teste de busca de paciente concluído.");
    }
}

