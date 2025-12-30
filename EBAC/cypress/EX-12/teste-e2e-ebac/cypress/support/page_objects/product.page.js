class ProductPage {
  selecionarSwatchPorClasse(valor) {
    // O plugin cria classes do tipo:
    // button-variable-item-XS, button-variable-item-Green, button-variable-item-Red ...
    const cls = `.button-variable-item-${valor}`;

    cy.get(cls, { timeout: 20000 })
      .first()
      .scrollIntoView()
      .click({ force: true });

    cy.wait(250);
  }

  selecionarVariacao(size, color) {
    // Seleciona Size e Color pelos swatches (classe do plugin)
    // IMPORTANTE: respeita exatamente o texto esperado nas classes (XS, S, L, Green, White, Blue, Red)
    this.selecionarSwatchPorClasse(size);
    this.selecionarSwatchPorClasse(color);

    // Valida pelo estado REAL do WooCommerce (mais confiável do que classe selected)
    cy.get('button.single_add_to_cart_button', { timeout: 20000 })
      .should('exist')
      .should(($btn) => {
        const disabled = $btn.is(':disabled') || $btn.hasClass('disabled');
        const needsSelection = $btn.hasClass('wc-variation-selection-needed');
        const unavailable = $btn.hasClass('wc-variation-is-unavailable');

        expect(needsSelection, 'Variação selecionada (não precisa mais selecionar)').to.eq(false);
        expect(unavailable, 'Combinação disponível (não indisponível)').to.eq(false);
        expect(disabled, 'Botão comprar habilitado').to.eq(false);
      });
  }

  definirQuantidade(qtd) {
    cy.get('input.qty', { timeout: 20000 })
      .clear({ force: true })
      .type(String(qtd), { force: true });
  }

  adicionarAoCarrinho() {
    cy.get('button.single_add_to_cart_button', { timeout: 20000 })
      .should('exist')
      .and('not.be.disabled')
      .click({ force: true });
  }

  irParaCarrinho() {
    cy.visit('/carrinho/');
  }
}

export default new ProductPage();
