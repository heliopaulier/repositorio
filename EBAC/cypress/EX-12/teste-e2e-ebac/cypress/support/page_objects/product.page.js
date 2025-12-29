class ProductPage {
  // ---------------- Helpers ----------------
  botaoComprarEstaHabilitado($btn) {
    return !($btn.is(':disabled') || $btn.hasClass('disabled'));
  }

  getBotaoComprar() {
    return cy.get('button.single_add_to_cart_button', { timeout: 20000 }).should('exist');
  }

  // ---------------- Variações por BOTÕES (swatches) ----------------
  configurarVariacoesPorBotoes() {
    // Tentativa robusta: procurar as opções de Size e Color pelos rótulos
    const getOptionsByLabel = (labelText) => {
      // Tenta achar a linha da tabela de variações pelo rótulo (Size/Color)
      // e dentro dela coletar as opções clicáveis.
      const row = Cypress.$('.variations tr').filter((_, tr) =>
        Cypress.$(tr).text().toLowerCase().includes(labelText.toLowerCase())
      );

      if (row.length) {
        const $row = Cypress.$(row[0]);
        const $opts = $row.find(
          '.variable-item:not(.disabled):not(.outofstock), li.variable-item:not(.disabled):not(.outofstock), button.variable-item:not(.disabled)'
        );
        return $opts.toArray();
      }

      // Fallback: pega wrappers em ordem (se não achou por label)
      const wrappers = Cypress.$(
        '.variations .variable-items-wrapper, .woo-variation-items-wrapper .variable-items-wrapper, .variable-items-wrapper'
      );
      if (!wrappers.length) return [];

      // labelText "size" -> primeiro wrapper, "color" -> segundo wrapper (fallback)
      const idx = labelText.toLowerCase().includes('size') ? 0 : 1;
      const $wrap = Cypress.$(wrappers.get(idx));
      const $opts = $wrap.find(
        '.variable-item:not(.disabled):not(.outofstock), li.variable-item:not(.disabled):not(.outofstock), button.variable-item:not(.disabled)'
      );
      return $opts.toArray();
    };

    cy.get('body').then(() => {
      const sizeOptions = getOptionsByLabel('size');
      const colorOptions = getOptionsByLabel('color');

      if (!sizeOptions.length || !colorOptions.length) {
        throw new Error(
          'Não consegui identificar opções de Size/Color por botões. Verifique o DOM dos swatches (classe variable-item).'
        );
      }

      // Tenta combinações até habilitar o botão
      const tryCombo = (si, ci) => {
        if (si >= sizeOptions.length) {
          throw new Error('Nenhuma combinação de variação habilitou o botão Comprar (produto pode estar sem estoque).');
        }

        const sizeEl = sizeOptions[si];
        const colorEl = colorOptions[ci];

        cy.wrap(sizeEl).scrollIntoView().click({ force: true });
        cy.wait(250);
        cy.wrap(colorEl).scrollIntoView().click({ force: true });
        cy.wait(400);

        return this.getBotaoComprar().then(($btn) => {
          if (this.botaoComprarEstaHabilitado($btn)) {
            return; // sucesso
          }

          const nextCi = ci + 1;
          if (nextCi < colorOptions.length) {
            return tryCombo(si, nextCi);
          }
          return tryCombo(si + 1, 0);
        });
      };

      return tryCombo(0, 0);
    });
  }

  // ---------------- Variações por SELECT (fallback) ----------------
  configurarVariacoesPorSelect() {
    cy.get('.variations select').each(($select) => {
      cy.wrap($select).then(($s) => {
        const options = [...$s[0].options]
          .filter((o) => o.value && o.value.trim().length > 0)
          .map((o) => o.value);

        if (!options.length) return;

        cy.wrap($s).select(options[0], { force: true });
      });
    });

    // Só segue se habilitar (se não habilitar, deixa o erro claro)
    this.getBotaoComprar().should(($btn) => {
      const ok = this.botaoComprarEstaHabilitado($btn);
      expect(ok, 'Botão comprar habilitado após selects').to.eq(true);
    });
  }

  // ---------------- Public API ----------------
  configurarVariacoesSeExistirem() {
    cy.get('body').then(($body) => {
      const hasSwatches =
        $body.find('.variable-items-wrapper').length > 0 ||
        $body.find('.woo-variation-items-wrapper').length > 0 ||
        $body.find('.variable-item').length > 0;

      const hasSelect = $body.find('.variations select').length > 0;

      // IMPORTANTE: se houver swatches, prioriza swatches (mesmo que existam selects ocultos)
      if (hasSwatches) {
        this.configurarVariacoesPorBotoes();
        return;
      }

      if (hasSelect) {
        this.configurarVariacoesPorSelect();
        return;
      }

      // Produto simples: não faz nada
    });
  }

  definirQuantidade(qtd) {
    cy.get('input.qty').clear({ force: true }).type(String(qtd), { force: true });
  }

  adicionarAoCarrinho() {
    this.getBotaoComprar()
      .should(($btn) => {
        const ok = this.botaoComprarEstaHabilitado($btn);
        expect(ok, 'Botão comprar habilitado antes do clique').to.eq(true);
      })
      .click({ force: true });
  }

  irParaCarrinho() {
    cy.visit('/carrinho/');
  }
}

export default new ProductPage();
