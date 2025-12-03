# Automação de Testes para Sistema de Gestão Hospitalar com SikuliX e Maven

Este projeto demonstra a automação de testes de interface gráfica (GUI) para um sistema de gestão hospitalar, utilizando a biblioteca SikuliX API, Maven para gerenciamento de projeto e JUnit para o framework de testes. O foco principal é o cadastro de pacientes, incluindo validação de campos, preenchimento com dados fake, geração de relatórios de métricas e visualização gráfica, além de uma estrutura para suite de testes e integração com CI/CD.

## 1. Visão Geral do Projeto

O objetivo deste projeto é fornecer uma solução robusta para testar sistemas legados ou aplicações onde a interação via elementos de interface gráfica tradicionais (como IDs de elementos HTML ou propriedades de objetos) não é viável. O SikuliX utiliza reconhecimento de imagem para interagir com a tela, tornando-o ideal para sistemas como Oracle Forms, que foram mencionados como o ambiente do sistema hospitalar.

### Funcionalidades Implementadas:
- **Automação de GUI**: Interação com elementos da tela através de reconhecimento de imagem (simulado em ambiente headless).
- **Geração de Dados Fake**: Utilização de uma classe utilitária para gerar dados de paciente realistas para testes.
- **Testes de Cadastro de Paciente**: Cenário de teste para preenchimento e validação de campos no formulário de cadastro de paciente.
- **Suite de Testes**: Estrutura para agrupar e executar múltiplos cenários de teste.
- **Relatórios de Teste**: Geração de relatórios detalhados com métricas de execução.
- **Visualização de Métricas**: Geração de gráficos visuais a partir dos resultados dos testes.
- **Integração CI/CD**: Configuração de um `Jenkinsfile` para automação da pipeline de testes.

## 2. Configuração do Ambiente

Para executar este projeto, você precisará das seguintes ferramentas instaladas:

- **Java Development Kit (JDK) 8 ou superior**: Necessário para compilar e executar o projeto Maven.
- **Apache Maven 3.x**: Ferramenta de automação de build e gerenciamento de dependências.
- **SikuliX API**: A biblioteca principal para automação de GUI. O JAR `sikulixapi-2.0.5.jar` é gerenciado via Maven.

### 2.1. Instalação do Java e Maven

Certifique-se de que o Java e o Maven estão instalados e configurados corretamente em seu sistema. Você pode verificar as versões com os seguintes comandos:

```bash
java -version
mvn -version
```

### 2.2. Download do SikuliX IDE (Opcional)

Embora a API seja usada diretamente no projeto Maven, o SikuliX IDE pode ser útil para capturar imagens e depurar scripts. Você pode baixar o JAR do IDE em:

[SikuliX Downloads](https://raiman.github.io/SikuliX1/downloads.html)

## 3. Estrutura do Projeto

O projeto segue a estrutura padrão de um projeto Maven:

```
hospital-test-automation/
├── pom.xml
├── Jenkinsfile
├── src/
│   └── test/
│       └── java/
│           └── com/
│               └── hospital/
│                   └── tests/
│                       ├── AppTest.java
│                       ├── BaseSikuliTest.java
│                       ├── ExampleSikuliTest.java
│                       ├── FakeDataGenerator.java
│                       ├── PatientRegistrationTest.java
│                       ├── PatientSearchTest.java
│                       └── PatientTestSuite.java
├── target/
│   └── surefire-reports/  # Relatórios de teste gerados
│   └── classes/
│   └── test-classes/
└── reports/
    └── test_metrics_graph.png # Gráfico de métricas gerado
└── generate_report_graph.py
```

- `pom.xml`: Arquivo de configuração do Maven, define dependências e plugins.
- `Jenkinsfile`: Script para a pipeline de CI/CD do Jenkins.
- `src/test/java/com/hospital/tests/`:
    - `BaseSikuliTest.java`: Classe base para os testes SikuliX, contendo métodos utilitários para interação com a tela e um modo headless para simulação.
    - `FakeDataGenerator.java`: Classe para gerar dados fake (nome, CPF, data de nascimento, etc.) para os pacientes.
    - `PatientRegistrationTest.java`: Teste de automação para o cenário de cadastro de paciente.
    - `PatientSearchTest.java`: Teste de automação para o cenário de busca de paciente.
    - `PatientTestSuite.java`: Uma suite de testes JUnit que agrupa `PatientRegistrationTest` e `PatientSearchTest`.
- `generate_report_graph.py`: Script Python para analisar os relatórios XML do Surefire e gerar um gráfico visual das métricas.

## 4. Executando os Testes Localmente

Para executar todos os testes definidos na `PatientTestSuite` e gerar os relatórios, navegue até o diretório raiz do projeto (`hospital-test-automation/`) e execute o seguinte comando Maven:

```bash
mvn clean test
```

Este comando irá:
1. Limpar o diretório `target`.
2. Compilar o código fonte e os testes.
3. Executar a `PatientTestSuite` (que inclui `PatientRegistrationTest` e `PatientSearchTest`).
4. Gerar os relatórios de teste no diretório `target/surefire-reports/`.

## 5. Geração de Relatórios e Gráficos

Após a execução dos testes, você pode gerar um gráfico visual das métricas de teste usando o script Python fornecido:

```bash
python3 generate_report_graph.py
```

Este script lerá os arquivos XML gerados pelo Surefire e criará um gráfico `test_metrics_graph.png` no diretório `reports/`.

## 6. Integração Contínua/Entrega Contínua (CI/CD)

O `Jenkinsfile` incluído no projeto define uma pipeline de CI/CD que pode ser utilizada com um servidor Jenkins. A pipeline consiste nas seguintes etapas:

- **Build**: Compila o projeto Maven.
- **Test**: Executa os testes JUnit/SikuliX.
- **Generate Reports**: Gera os relatórios de teste e o gráfico de métricas.
- **Archive Reports**: Arquiva os relatórios e o gráfico para acesso posterior no Jenkins.

Para configurar esta pipeline no Jenkins:
1. Instale o plugin Pipeline no Jenkins.
2. Crie um novo item do tipo **Pipeline** no Jenkins.
3. Configure o SCM (Source Code Management) para apontar para o seu repositório Git onde este projeto está hospedado.
4. No campo "Script Path" da configuração da Pipeline, especifique `Jenkinsfile`.

## 7. Configuração do VSCode

Para uma experiência de desenvolvimento otimizada no VSCode, recomendamos as seguintes extensões:

- **Extension Pack for Java**: Inclui Language Support for Java™ by Red Hat, Debugger for Java, Maven for Java, entre outros.
- **SikuliX Extension (se disponível)**: Embora não haja uma extensão oficial robusta para SikuliX no VSCode, você pode configurar o VSCode para realçar a sintaxe Python ou Java (dependendo de como você escreve seus scripts SikuliX) e usar ferramentas externas para captura de imagens.

### Dicas para VSCode:
- **Configuração de Build**: Você pode configurar tarefas de build no VSCode para executar comandos Maven diretamente, como `mvn clean install` ou `mvn test`.
- **Depuração**: Utilize as ferramentas de depuração do Java para depurar seus testes JUnit/SikuliX.
- **Captura de Imagens**: Para capturar as imagens que o SikuliX usará, você precisará do SikuliX IDE ou de uma ferramenta de captura de tela externa. As imagens devem ser salvas em um diretório acessível pelo projeto (por exemplo, `src/test/resources/images`).

## 8. Considerações sobre Oracle Forms e SikuliX

Conforme mencionado, o sistema de gestão hospitalar é desenvolvido em Oracle Forms. Isso significa que a interação com a interface é feita exclusivamente através de reconhecimento de imagem (SikuliX) ou OCR (Optical Character Recognition). As imagens fornecidas (`pasted_file_byvdeG_image.png`, `pasted_file_PdlYbR_image.png`, `pasted_file_1OxWRt_image.png`) são exemplos das telas que seriam automatizadas.

Ao desenvolver testes para Oracle Forms com SikuliX, é crucial:
- **Capturar imagens precisas**: Pequenas variações na interface podem causar falhas no reconhecimento.
- **Usar regiões (Regions)**: Definir áreas específicas da tela para buscar imagens, melhorando a performance e a robustez.
- **Implementar OCR**: Para textos dinâmicos ou campos onde a imagem não é consistente, o OCR pode ser uma alternativa.
- **Tratar tempos de espera**: Sistemas Oracle Forms podem ter tempos de carregamento variáveis, exigindo esperas adequadas (`waitImage`).

## 9. Próximos Passos e Melhorias

Este projeto serve como base e pode ser expandido com as seguintes melhorias:

- **Integração de OCR**: Adicionar bibliotecas de OCR (como Tesseract via Tess4J) para reconhecimento de texto em elementos dinâmicos da tela.
- **Relatórios Mais Detalhados**: Integrar com ferramentas de relatório mais avançadas, como Allure Reports, para visualizações interativas.
- **Geração de Dados Mais Complexa**: Implementar geradores de dados fake mais sofisticados, com validação de regras de negócio.
- **Mais Cenários de Teste**: Expandir a suite de testes para cobrir outros módulos do sistema hospitalar (agendamento, faturamento, etc.).
- **Parametrização de Testes**: Permitir a execução dos mesmos testes com diferentes conjuntos de dados.
- **Dockerização**: Empacotar o ambiente de execução dos testes em containers Docker para garantir consistência entre ambientes.

---

**Autor**: Manus AI
**Data**: 14 de Outubro de 2025
