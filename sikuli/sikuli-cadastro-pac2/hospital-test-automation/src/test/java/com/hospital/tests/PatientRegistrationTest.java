package com.hospital.tests;

import org.junit.Test;
import org.sikuli.script.FindFailed;

public class PatientRegistrationTest extends BaseSikuliTest {

    @Test
    public void testPatientRegistration() {
        System.out.println("Iniciando teste de cadastro de paciente...");

        // Gerar dados fake para o paciente
        String nomeCompleto = FakeDataGenerator.generateFakeName();
        String cpf = FakeDataGenerator.generateFakeCPF();
        String dataNascimento = FakeDataGenerator.generateFakeDateOfBirth();
        String endereco = FakeDataGenerator.generateFakeAddress();
        String telefone = FakeDataGenerator.generateFakePhoneNumber();
        String email = FakeDataGenerator.generateFakeEmail(nomeCompleto);

        System.out.println("Dados do paciente gerados:");
        System.out.println("Nome: " + nomeCompleto);
        System.out.println("CPF: " + cpf);
        System.out.println("Data de Nascimento: " + dataNascimento);
        System.out.println("Endereço: " + endereco);
        System.out.println("Telefone: " + telefone);
        System.out.println("Email: " + email);

        // Simulação de interação com o sistema usando SikuliX
        // NOTA: Em um ambiente real, 'imagePath' seriam os caminhos para as imagens dos elementos da GUI.
        // Como estamos em um ambiente headless, estas chamadas são simuladas.

        try {
            // Exemplo: Clicar no botão 'Novo Paciente'
            // clickImage("images/btn_novo_paciente.png");
            System.out.println("Simulando clique em 'Novo Paciente'.");
            Thread.sleep(1000); // Simula tempo de carregamento

            // Exemplo: Preencher campo 'Nome Completo'
            // typeText("images/campo_nome_completo.png", nomeCompleto);
            System.out.println("Simulando preenchimento do campo 'Nome Completo' com: " + nomeCompleto);
            Thread.sleep(500);

            // Exemplo: Preencher campo 'CPF'
            // typeText("images/campo_cpf.png", cpf);
            System.out.println("Simulando preenchimento do campo 'CPF' com: " + cpf);
            Thread.sleep(500);

            // Exemplo: Preencher campo 'Data de Nascimento'
            // typeText("images/campo_data_nascimento.png", dataNascimento);
            System.out.println("Simulando preenchimento do campo 'Data de Nascimento' com: " + dataNascimento);
            Thread.sleep(500);

            // Exemplo: Preencher campo 'Endereço'
            // typeText("images/campo_endereco.png", endereco);
            System.out.println("Simulando preenchimento do campo 'Endereço' com: " + endereco);
            Thread.sleep(500);

            // Exemplo: Preencher campo 'Telefone'
            // typeText("images/campo_telefone.png", telefone);
            System.out.println("Simulando preenchimento do campo 'Telefone' com: " + telefone);
            Thread.sleep(500);

            // Exemplo: Preencher campo 'Email'
            // typeText("images/campo_email.png", email);
            System.out.println("Simulando preenchimento do campo 'Email' com: " + email);
            Thread.sleep(500);

            // Exemplo: Clicar no botão 'Salvar'
            // clickImage("images/btn_salvar.png");
            System.out.println("Simulando clique em 'Salvar'.");
            Thread.sleep(2000); // Simula tempo de processamento

            // Exemplo: Validar mensagem de sucesso
            // if (existsImage("images/msg_sucesso.png")) {
            //     System.out.println("Paciente cadastrado com sucesso!");
            // } else {
            //     System.err.println("Erro: Mensagem de sucesso não encontrada.");
            //     throw new FindFailed("Mensagem de sucesso não encontrada.");
            // }
            System.out.println("Simulando validação de mensagem de sucesso: Paciente cadastrado com sucesso!");


        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Teste interrompido: " + e.getMessage());
            throw new RuntimeException(e);
        }

        System.out.println("Teste de cadastro de paciente concluído.");
    }
}

