class HomePage {
  visitar() {
    cy.visit('https://demoqa.com/')

    // Remove anúncios do Google que ficam em iframe
    cy.get('iframe[id^="google_ads"]', { timeout: 1000 })
      .then($ads => {
        if ($ads.length) {
          cy.wrap($ads).invoke('remove')
        }
      })
  }

  clicarForms() {
    cy.contains('.card.mt-4.top-card', 'Forms').click()
  }
}

export default new HomePage()
