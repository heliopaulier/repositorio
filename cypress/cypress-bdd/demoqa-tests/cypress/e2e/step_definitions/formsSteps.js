import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor';
import HomePage from '../../support/page_objects/homePage';
import FormsPage from '../../support/page_objects/formsPage';

Given('que o usuário acessa o site DemoQA', () => {
  HomePage.visitarHome();
});

When('o usuário navega até o menu Forms e abre o Practice Form', () => {
  HomePage.clicarForms();
  FormsPage.clicarPracticeForm();
});

When('preenche todos os campos do formulário com dados válidos', () => {
  FormsPage.preencherFormulario();
});

When('realiza o upload de um arquivo txt', () => {
  // já feito no preenchimento
});

When('submete o formulário', () => {
  FormsPage.submeterFormulario();
});

Then('deve visualizar o popup de confirmação', () => {
  FormsPage.validarPopup();
});

Then('fecha o popup com sucesso', () => {
  FormsPage.fecharPopup();
});
