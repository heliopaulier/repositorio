class CheckoutPage {
  preencherDadosFaturamento(dados) {
    cy.get('#billing_first_name', { timeout: 20000 }).clear().type(dados.nome);
    cy.get('#billing_last_name').clear().type(dados.sobrenome);

    cy.get('#billing_address_1').clear().type(dados.endereco);
    cy.get('#billing_city').clear().type(dados.cidade);
    cy.get('#billing_postcode').clear().type(dados.cep);

    cy.get('#billing_phone').clear().type(dados.telefone);
    cy.get('#billing_email').clear().type(dados.email);

    // Se existir país/estado, preenche (alguns temas escondem ou mudam)
    cy.get('body').then(($body) => {
      if ($body.find('#billing_country').length) {
        cy.get('#billing_country').select(dados.pais, { force: true });
      }

      if ($body.find('#billing_state').length) {
        const $state = $body.find('#billing_state');
        if ($state.is('select')) {
          cy.get('#billing_state').select(dados.estado, { force: true });
        } else {
          cy.get('#billing_state').clear().type(dados.estado);
        }
      }
    });
  }

  selecionarPagamentoPorTransferencia() {
    // Preferência: transferência (bacs). Se não existir, tenta "cod".
    cy.get('body').then(($body) => {
      if ($body.find('#payment_method_bacs').length) {
        cy.get('#payment_method_bacs').check({ force: true });
        return;
      }
      if ($body.find('#payment_method_cod').length) {
        cy.get('#payment_method_cod').check({ force: true });
      }
    });
  }

  finalizarPedido() {
    cy.get('#place_order', { timeout: 20000 })
      .should('be.visible')
      .click();
  }

  validarPedidoRealizado() {
    // WooCommerce padrão: notice de sucesso OU bloco de pedido
    cy.get('body', { timeout: 20000 }).then(($body) => {
      const hasSuccess =
        $body.find('.woocommerce-notice--success').length > 0 ||
        $body.find('.woocommerce-order').length > 0;

      expect(hasSuccess, 'Página de pedido concluído exibida').to.eq(true);
    });
  }
}

export default new CheckoutPage();
