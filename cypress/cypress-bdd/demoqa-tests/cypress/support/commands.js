// Fecha automaticamente pop-ups ou iframes indesejados
Cypress.Commands.add('fecharPopups', () => {
  cy.window().then((win) => {
    const modais = win.document.querySelectorAll('iframe, .advertisement, .modal, #close-fixedban');
    modais.forEach(m => m.remove());
  });
});

// Visita o site base e fecha pop-ups iniciais
Cypress.Commands.add('acessarDemoQA', () => {
  cy.visit('/');
  cy.fecharPopups();
});
