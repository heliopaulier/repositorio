class HomePage {
  abrirCarrinho() {
    cy.visit('/carrinho/');
  }
}

export default new HomePage();
