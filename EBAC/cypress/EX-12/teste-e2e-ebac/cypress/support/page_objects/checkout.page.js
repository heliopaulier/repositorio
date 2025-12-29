class CheckoutPage {
    preencherDadosFaturamento(dados) {
      // Campos padrão WooCommerce (billing)
      cy.get('#billing_first_name').clear().type(dados.nome);
      cy.get('#billing_last_name').clear().type(dados.sobrenome);
  
      cy.get('#billing_address_1').clear().type(dados.endereco);
      cy.get('#billing_city').clear().type(dados.cidade);
      cy.get('#billing_postcode').clear().type(dados.cep);
      cy.get('#billing_phone').clear().type(dados.telefone);
      cy.get('#billing_email').clear().type(dados.email);
  
      // Alguns temas pedem estado/país; se existir, preenche.
      cy.get('body').then($body => {
        if ($body.find('#billing_country').length) {
          cy.get('#billing_country').select(dados.pais, { force: true });
        }
        if ($body.find('#billing_state').length) {
          // Se for select, seleciona; se for input, digita.
          const $state = $body.find('#billing_state');
          if ($state.is('select')) cy.get('#billing_state').select(dados.estado, { force: true });
          else cy.get('#billing_state').clear().type(dados.estado);
        }
      });
    }
  
    selecionarPagamentoPorTransferencia() {
      // Métodos comuns: bacs (transferência), cod (na entrega), cheque etc.
      cy.get('body').then($body => {
        if ($body.find('#payment_method_bacs').length) {
          cy.get('#payment_method_bacs').check({ force: true });
        } else if ($body.find('#payment_method_cod').length) {
          cy.get('#payment_method_cod').check({ force: true });
        }
      });
    }
  
    finalizarPedido() {
      cy.get('#place_order').should('be.enabled').click();
    }
  
    validarPedidoRealizado() {
      // Página padrão de sucesso WooCommerce
      cy.get('.woocommerce-notice--success, .woocommerce-order')
        .should('be.visible');
    }
  }
  
  export default new CheckoutPage();
  