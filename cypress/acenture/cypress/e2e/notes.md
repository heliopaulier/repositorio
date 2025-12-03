tenho o teste abaixo e esta com erro da imagem. consegue me auxiliar com o teste:

📂 Estrutura sugerida
cypress/
  e2e/
    forms.cy.js
  fixtures/
    dados.json
    arquivo.txt
  support/
    page_objects/
      homePage.js
      formsPage.js
    commands.js

📄 Fixture de dados (cypress/fixtures/dados.json)
{
  "firstName": "João",
  "lastName": "Silva",
  "email": "joao.silva@example.com",
  "gender": "Male",
  "mobile": "11987654321",
  "dateOfBirth": "10 Jan 1990",
  "subjects": ["Maths", "English"],
  "hobbies": ["Sports", "Reading"],
  "address": "Rua Exemplo, 123 - São Paulo",
  "state": "NCR",
  "city": "Delhi"
}

📄 Page Object – HomePage (cypress/support/page_objects/homePage.js)
class HomePage {
  visitar() {
    cy.visit('https://demoqa.com/')
  }

  clicarForms() {
    cy.contains('.card-body h5', 'Forms').click()
  }
}

export default new HomePage()

📄 Page Object – FormsPage (cypress/support/page_objects/formsPage.js)
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


📄 Teste (cypress/e2e/forms.cy.js)
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
      formsPage.submeter()
      formsPage.validarPopup()
      formsPage.fecharPopup()
    })
  })
})


✅ Com isso o fluxo fica todo automatizado:

Acessa https://demoqa.com/

Vai em Forms → Practice Form

Preenche dados do fixture dados.json

Faz upload do arquivo.txt que está em cypress/fixtures/

Submete

Valida popup

Fecha popup


______________________________________________________________________________________________
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



    // ✅ Data de nascimento dinâmica
    // Abre o calendário
cy.get('#dateOfBirthInput').click()

// Seleciona ano
cy.get('.react-datepicker__year-select').select('1990')

// Seleciona mês
cy.get('.react-datepicker__month-select').select('December')

// Seleciona o dia
cy.get('.react-datepicker__day--012').click() // dia 12



  

    // Preenchimento de matérias
    dados.subjects.forEach((subject) => {
      cy.get('#subjectsInput').type(`${subject}{enter}`)
    })

    // Hobbies
    dados.hobbies.forEach((hobby) => {
      cy.contains('.custom-control-label', hobby).click()
    })

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


/// <reference types="cypress" />

import homePage from '../support/page_objects/homePage'
import formsPage from '../support/page_objects/formsPage'

describe('Fluxo completo de formulário', () => {

  // Ignora erros de scripts externos (ex: anúncios, iframes de terceiros)
  Cypress.on('uncaught:exception', (err, runnable) => {
    return false
  })

  beforeEach(() => {
    homePage.visitar()
  })

  it('Deve preencher e submeter o formulário', () => {
    cy.fixture('dados').then((dados) => {
      homePage.clicarForms()
      formsPage.clicarPracticeForm()
      formsPage.preencherFormulario(dados)
      formsPage.submeter()
      formsPage.validarPopup()
      formsPage.fecharPopup()
    })
  })
})
