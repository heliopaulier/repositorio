/// <reference types="cypress" />

import homePage from '../support/page_objects/home.page';
import productPage from '../support/page_objects/product.page';
import cartPage from '../support/page_objects/cart.page';
import checkoutPage from '../support/page_objects/checkout.page';

context('Exercicio - Testes End-to-end - Fluxo de pedido', () => {
  const dadosCheckout = {
    nome: 'Helio',
    sobrenome: 'Paulier',
    endereco: 'Rua Exemplo, 123',
    cidade: 'Sao Paulo',
    cep: '01001000',
    telefone: '11999999999',
    email: `helio.qa+${Date.now()}@email.com`,
    pais: 'BR',
    estado: 'SP',
  };

  it('Deve fazer um pedido na loja Ebac Shop de ponta a ponta', () => {
    const alvo = 4;            // quantos produtos queremos no carrinho
    const maxTentativas = 30;  // evita loop infinito se o ambiente estiver ruim

    let adicionados = 0;
    let indice = 0;

    /**
     * Tenta adicionar o produto do índice atual.
     * Se falhar (produto/variação sem estoque), NÃO derruba o teste.
     * Incrementa o índice e segue tentando até atingir "alvo".
     */
    const tentarAdicionarProduto = () => {
      if (adicionados >= alvo) return; // já completou

      if (indice >= maxTentativas) {
        throw new Error(
          `Não foi possível adicionar ${alvo} produtos após ${maxTentativas} tentativas. Possível falta de estoque no ambiente.`
        );
      }

      cy.log(`Tentando produto índice ${indice} (adicionados: ${adicionados}/${alvo})`);

      homePage.visitarLoja();
      homePage.abrirProdutoPorIndice(indice);

      // Vamos "capturar" falhas somente nesta tentativa.
      let falhou = false;

      const failHandler = (err) => {
        falhou = true;
        // Retorna false para impedir que o Cypress quebre o teste aqui
        // (assim conseguimos pular e ir para o próximo produto)
        return false;
      };

      Cypress.once('fail', failHandler);

      // Executa a tentativa de compra
      cy.then(() => {
        productPage.configurarVariacoesSeExistirem();
        productPage.definirQuantidade(1);
        productPage.adicionarAoCarrinho();
      }).then(() => {
        if (falhou) {
          cy.log(`Produto índice ${indice} indisponível. Pulando para o próximo.`);
          indice++;
          return tentarAdicionarProduto();
        }

        // Sucesso: vai ao carrinho para consolidar e contar
        productPage.irParaCarrinho();

        // Confirma que existe pelo menos 1 item (garantia mínima)
        cartPage.validarCarrinhoComItens();

        adicionados++;
        cy.log(`Produto adicionado com sucesso. Total: ${adicionados}/${alvo}`);

        indice++;
        return tentarAdicionarProduto();
      });
    };

    // Inicia o processo de adicionar produtos
    tentarAdicionarProduto();

    // Após adicionar 4 produtos, segue checkout
    cy.then(() => {
      homePage.abrirCarrinho();
      cartPage.validarCarrinhoComItens();
      cartPage.irParaCheckout();

      checkoutPage.preencherDadosFaturamento(dadosCheckout);
      checkoutPage.selecionarPagamentoPorTransferencia();
      checkoutPage.finalizarPedido();
      checkoutPage.validarPedidoRealizado();
    });
  });
});
