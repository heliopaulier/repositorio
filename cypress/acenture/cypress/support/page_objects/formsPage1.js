class FormsPage {
  clicarPracticeForm() {
    cy.contains('Practice Form').click()
  }

  preencherFormulario(dados) {
    cy.get('#firstName').type(dados.firstName)
    cy.get('#lastName').type(dados.lastName)
    cy.get('#userEmail').type(dados.email)
    cy.get(`input[name="gender"][value="${dados.gender}"]`).check({ force: true })
    cy.get('#userNumber').type(dados.mobile)

    // Upload do arquivo (deve estar em cypress/fixtures/)
    cy.get('#uploadPicture').selectFile('cypress/fixtures/arquivo.txt')

    cy.get('#currentAddress').type(dados.address)

    // Estado e Cidade
    cy.get('#state').click()
    cy.contains(dados.state).click()
    cy.get('#city').click()
    cy.contains(dados.city).click()
  }

  submeter() {
    cy.get('#submit').click({ force: true })
  }

  validarPopup() {
    cy.get('.modal-content').should('be.visible')
  }

  fecharPopup() {
    cy.get('#closeLargeModal').click({ force: true })
  }
}

export default new FormsPage()