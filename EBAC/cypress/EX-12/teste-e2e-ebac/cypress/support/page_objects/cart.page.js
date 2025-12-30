class CartPage {
  validarCarrinhoComItens() {
    cy.get('form.woocommerce-cart-form', { timeout: 20000 }).should('be.visible');
    cy.get('tr.woocommerce-cart-form__cart-item', { timeout: 20000 })
      .should('have.length.greaterThan', 0);
  }

  validarQuantidadeItens(quantidade) {
    cy.get('tr.woocommerce-cart-form__cart-item', { timeout: 20000 })
      .should('have.length', quantidade);
  }

  irParaCheckout() {
    cy.get('a.checkout-button', { timeout: 20000 })
      .should('be.visible')
      .click();
  }
}

export default new CartPage();
