package com.hospital.tests;

import java.util.Random;

public class FakeDataGenerator {

    private static final String[] FIRST_NAMES = {"João", "Maria", "Pedro", "Ana", "Carlos", "Sofia", "Lucas", "Laura"};
    private static final String[] LAST_NAMES = {"Silva", "Santos", "Oliveira", "Souza", "Pereira", "Almeida", "Costa", "Rodrigues"};
    private static final String[] CITIES = {"São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre", "Curitiba", "Salvador"};
    private static final String[] STREETS = {"Rua A", "Avenida B", "Travessa C", "Alameda D", "Praça E"};

    private static Random random = new Random();

    public static String generateFakeName() {
        return FIRST_NAMES[random.nextInt(FIRST_NAMES.length)] + " " + LAST_NAMES[random.nextInt(LAST_NAMES.length)];
    }

    public static String generateFakeCPF() {
        StringBuilder cpf = new StringBuilder();
        for (int i = 0; i < 11; i++) {
            cpf.append(random.nextInt(10));
        }
        return cpf.toString();
    }

    public static String generateFakeDateOfBirth() {
        int year = 1950 + random.nextInt(50); // 1950-1999
        int month = 1 + random.nextInt(12);
        int day = 1 + random.nextInt(28); // Simplificado para evitar validação de dias em meses
        return String.format("%02d/%02d/%d", day, month, year);
    }

    public static String generateFakeAddress() {
        return STREETS[random.nextInt(STREETS.length)] + ", " + (1 + random.nextInt(999)) + " - " + CITIES[random.nextInt(CITIES.length)];
    }

    public static String generateFakePhoneNumber() {
        return String.format("(%02d) 9%04d-%04d", 11 + random.nextInt(90), random.nextInt(10000), random.nextInt(10000));
    }

    public static String generateFakeEmail(String name) {
        String cleanName = name.toLowerCase().replaceAll("\\s+", ".");
        return cleanName + random.nextInt(1000) + "@example.com";
    }
}

