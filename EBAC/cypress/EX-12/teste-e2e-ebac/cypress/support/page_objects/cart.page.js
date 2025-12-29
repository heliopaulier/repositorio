class CartPage {
    validarCarrinhoComItens() {
      // Tabela do carrinho padrão WooCommerce
      cy.get('form.woocommerce-cart-form').should('be.visible');
      cy.get('tr.woocommerce-cart-form__cart-item').should('have.length.greaterThan', 0);
    }
  
    irParaCheckout() {
      cy.get('a.checkout-button, a.wc-proceed-to-checkout a')
        .first()
        .should('be.visible')
        .click();
    }
  }
  
  export default new CartPage();
  