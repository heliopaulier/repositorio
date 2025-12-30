/// <reference types="cypress" />

import homePage from '../support/page_objects/home.page';
import productPage from '../support/page_objects/product.page';
import cartPage from '../support/page_objects/cart.page';
import checkoutPage from '../support/page_objects/checkout.page';

context('Exercicio - Testes End-to-end - Fluxo de pedido (didático)', () => {
  it('Deve comprar 4 produtos específicos com estoque e finalizar o pedido', () => {
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

    const produtos = [
      {
        url: 'http://lojaebac.ebaconline.art.br/product/ajax-full-zip-sweatshirt/',
        size: 'XS',
        color: 'Green',
      },
      {
        url: 'http://lojaebac.ebaconline.art.br/product/selene-yoga-hoodie/',
        size: 'S',
        color: 'White',
      },
      {
        url: 'http://lojaebac.ebaconline.art.br/product/tristan-endurance-tank/',
        size: 'L',
        color: 'Red',
      },
      {
        url: 'http://lojaebac.ebaconline.art.br/product/zoltan-gym-tee/',
        size: 'S',
        color: 'Blue',
      },
    ];

    // 1) Adiciona os 4 produtos (determinístico)
    produtos.forEach((p) => {
      cy.visit(p.url);

      productPage.selecionarVariacao(p.size, p.color);
      productPage.definirQuantidade(1);
      productPage.adicionarAoCarrinho();

      // Para não depender de mensagem "View cart"
      productPage.irParaCarrinho();
    });

    // 2) Valida carrinho
    homePage.abrirCarrinho();
    cartPage.validarCarrinhoComItens();
    cartPage.validarQuantidadeItens(4);

    // 3) Checkout
    cartPage.irParaCheckout();
    checkoutPage.preencherDadosFaturamento(dadosCheckout);
    checkoutPage.selecionarPagamentoPorTransferencia();
    checkoutPage.finalizarPedido();

    // 4) Validação final (pedido concluído)
    checkoutPage.validarPedidoRealizado();
  });
});
