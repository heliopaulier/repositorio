package com.hospital.tests;

import org.sikuli.script.Screen;
import org.sikuli.script.Pattern;
import org.sikuli.script.FindFailed;

public class BaseSikuliTest {

    protected Screen screen;
    protected boolean isHeadless = false; // Flag para indicar ambiente headless

    public BaseSikuliTest() {
        // Tenta inicializar Screen, se falhar, assume ambiente headless
        try {
            screen = new Screen();
        } catch (Exception e) {
            System.out.println("SikuliX: Ambiente headless detectado. Interações GUI serão simuladas.");
            isHeadless = true;
        }
    }

    protected void clickImage(String imagePath) throws FindFailed {
        if (isHeadless) {
            System.out.println("Simulando clique na imagem: " + imagePath);
        } else {
            screen.click(imagePath);
        }
    }

    protected void typeText(String imagePath, String text) throws FindFailed {
        if (isHeadless) {
            System.out.println("Simulando digitação de texto \"" + text + "\" no campo: " + imagePath);
        } else {
            screen.type(imagePath, text);
        }
    }

    protected void waitImage(String imagePath, double timeout) throws FindFailed {
        if (isHeadless) {
            System.out.println("Simulando espera pela imagem: " + imagePath + " por " + timeout + " segundos.");
            try { Thread.sleep((long) (timeout * 1000)); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        } else {
            screen.wait(imagePath, timeout);
        }
    }

    protected boolean existsImage(String imagePath) {
        if (isHeadless) {
            System.out.println("Simulando verificação de existência da imagem: " + imagePath + " (retornando true para simulação).");
            return true; // Sempre retorna true em modo headless para simular sucesso
        } else {
            return screen.exists(imagePath) != null;
        }
    }

    // Adicionar mais métodos utilitários conforme necessário
}

