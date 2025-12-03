class HomePage {
  visitarHome() {
    cy.acessarDemoQA();
  }

  clicarForms() {
    cy.contains('.card-body h5', 'Forms').click();
  }
}

export default new HomePage();
