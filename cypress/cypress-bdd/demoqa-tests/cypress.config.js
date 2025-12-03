const { defineConfig } = require('cypress');
const createBundler = require('@bahmutov/cypress-esbuild-preprocessor');
const addCucumberPreprocessorPlugin = require('@badeball/cypress-cucumber-preprocessor').addCucumberPreprocessorPlugin;
const createEsbuildPlugin = require('@badeball/cypress-cucumber-preprocessor/esbuild').createEsbuildPlugin;

module.exports = defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/features/*.feature',
    supportFile: 'cypress/support/commands.js',
    setupNodeEvents(on, config) {
      on('file:preprocessor', createBundler({
        plugins: [createEsbuildPlugin(config)],
      }));

      addCucumberPreprocessorPlugin(on, config);
      return config;
    },
    baseUrl: 'https://demoqa.com',
    chromeWebSecurity: false
  },
});
