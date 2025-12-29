class HomePage {
  visitarLoja() {
    cy.visit('/produtos/');
  }

  // Retorna o seletor correto dos "cards" de produto, independente do tema
  getListaProdutos() {
    return cy.get('body', { timeout: 20000 }).then(($body) => {
      // WooCommerce clássico
      if ($body.find('ul.products li.product').length) {
        return cy.get('ul.products li.product', { timeout: 20000 });
      }

      // Alguns temas usam divs ao invés de li
      if ($body.find('.products .product').length) {
        return cy.get('.products .product', { timeout: 20000 });
      }

      // WooCommerce Blocks (Gutenberg)
      if ($body.find('.wc-block-grid__products .wc-block-grid__product').length) {
        return cy.get('.wc-block-grid__products .wc-block-grid__product', { timeout: 20000 });
      }

      // Se cair aqui, significa que o tema usa outro HTML (aí a gente ajusta com base no DOM real)
      throw new Error(
        'Não encontrei a grade de produtos. Verifique o DOM e ajuste o seletor no HomePage.getListaProdutos().'
      );
    });
  }

  abrirProdutoPorIndice(index) {
    this.getListaProdutos()
      .should('have.length.greaterThan', index)
      .eq(index)
      .within(() => {
        // tenta achar um link clicável do produto
        cy.get('a')
          .first()
          .click({ force: true });
      });
  }

  abrirCarrinho() {
    cy.visit('/carrinho/');
  }
}

export default new HomePage();
