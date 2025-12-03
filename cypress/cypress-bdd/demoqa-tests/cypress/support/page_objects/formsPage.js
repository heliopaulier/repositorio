import { faker } from '@faker-js/faker';

class FormsPage {
  clicarPracticeForm() {
    cy.contains('Practice Form').click();
  }

  preencherFormulario() {
    cy.get('#firstName').type(faker.person.firstName());
    cy.get('#lastName').type(faker.person.lastName());
    cy.get('#userEmail').type(faker.internet.email());
    cy.get('label[for="gender-radio-1"]').click();
    cy.get('#userNumber').type(faker.number.int({ min: 1000000000, max: 9999999999 }).toString());
    cy.get('#dateOfBirthInput').click();
    cy.get('.react-datepicker__year-select').select('1995');
    cy.get('.react-datepicker__month-select').select('May');
    cy.get('.react-datepicker__day--015').click();
    cy.get('#subjectsInput').type('Maths{enter}');
    cy.get('label[for="hobbies-checkbox-1"]').click();
    cy.get('#uploadPicture').selectFile('cypress/fixtures/arquivo.txt');
    cy.get('#currentAddress').type(faker.location.streetAddress());
    cy.get('#react-select-3-input').type('NCR{enter}');
    cy.get('#react-select-4-input').type('Delhi{enter}');
  }

  submeterFormulario() {
    cy.get('#submit').click({ force: true });
  }

  validarPopup() {
    cy.get('.modal-content').should('be.visible');
  }

  fecharPopup() {
    cy.get('#closeLargeModal').click({ force: true });
  }
}

export default new FormsPage();
