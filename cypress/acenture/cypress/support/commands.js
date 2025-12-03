Cypress.Commands.add('removerAds', () => {
  cy.get('iframe[id^="google_ads"]', { timeout: 1000 }).then($ads => {
    if ($ads.length) {
      cy.wrap($ads).invoke('remove')
    }
  })
})

  
Cypress.Commands.add('fecharPopupSeExistir', (selector) => {
  cy.get('body').then($body => {
    if ($body.find(selector).length > 0) {
      cy.get(selector).click({ force: true })
    }
  })
})









// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })