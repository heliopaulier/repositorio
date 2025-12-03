package com.hospital.tests;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
    PatientRegistrationTest.class,
    PatientSearchTest.class
})
public class PatientTestSuite {
    // Esta classe não precisa de corpo, é apenas um contêiner para a suite de testes.
}

