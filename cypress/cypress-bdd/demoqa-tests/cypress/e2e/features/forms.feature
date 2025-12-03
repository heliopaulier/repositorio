Feature: Formulário de cadastro no site DemoQA

  Scenario: Preencher e submeter o formulário com sucesso
    Given que o usuário acessa o site DemoQA
    When o usuário navega até o menu Forms e abre o Practice Form
    And preenche todos os campos do formulário com dados válidos
    And realiza o upload de um arquivo txt
    And submete o formulário
    Then deve visualizar o popup de confirmação
    And fecha o popup com sucesso
