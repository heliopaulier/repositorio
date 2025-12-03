/// <reference types="cypress" />

import homePage from '../support/page_objects/homePage'
import formsPage from '../support/page_objects/formsPage'

describe('Fluxo completo de formulário', () => {
  beforeEach(() => {
    homePage.visitar()
  })

  it('Deve preencher e submeter o formulário', () => {
    cy.fixture('dados').then((dados) => {
      // Fluxo
      homePage.clicarForms()
      formsPage.clicarPracticeForm()
      formsPage.preencherFormulario(dados)
      //formsPage.submeter()
      //formsPage.validarPopup()
      //formsPage.fecharPopup()
    })
  })
})