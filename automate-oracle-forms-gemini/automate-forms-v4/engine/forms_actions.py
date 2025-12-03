# engine/forms_actions.py

import pyautogui
import time
from pathlib import Path
from ia.ia_helper import ocr_locate_by_text
from ia.ia_visao import template_match_location

# Configuração do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25 # Pequena pausa entre cada ação

# Diretório para onde as evidências serão salvas.
EVIDENCE_DIR = Path('reports/evidencia')
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR = Path('templates')

class FormsActions:
    
    def __init__(self):
        # Limpar o diretório de evidências ao iniciar (opcional)
        # for f in EVIDENCE_DIR.glob('*'): os.remove(f)
        pass

    def screenshot(self, prefix='screen'):
        """Tira uma screenshot e salva no diretório de evidências."""
        ts = time.strftime('%Y%m%d_%H%M%S')
        path = str(EVIDENCE_DIR / f"{prefix}_{ts}.png")
        pyautogui.screenshot(path)
        return path

    def click_xy(self, x, y, duration=0.2):
        """Move o mouse e clica em uma coordenada específica."""
        pyautogui.moveTo(x, y, duration=duration)
        pyautogui.click()

    def type_text(self, text):
        """Digita um texto na posição atual do cursor."""
        pyautogui.write(text, interval=0.03)

    def press(self, key):
        """Pressiona uma tecla (ex: 'enter', 'tab', 'f10')."""
        pyautogui.press(key)

    # --- FUNÇÕES DE LOCALIZAÇÃO INTELIGENTE ---

    def wait_and_click_by_text(self, text_to_find: str, timeout: int = 20, confidence_threshold: int = 70) -> bool:
        """
        Espera até que um texto seja encontrado via OCR na tela e clica no seu centro.
        Faz tentativas a cada 1 segundo.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_screen_path = self.screenshot('wait_ocr_temp')
            x, y, conf = ocr_locate_by_text(current_screen_path, text_to_find)
            
            if x is not None and conf >= confidence_threshold:
                self.click_xy(x, y)
                self.screenshot(f"click_ocr_{text_to_find.replace(' ', '_')}")
                print(f"✅ OCR Clicado em '{text_to_find}' (Conf: {conf})")
                return True
            
            time.sleep(1)
        
        print(f"❌ ERRO: Texto '{text_to_find}' não encontrado via OCR após {timeout}s.")
        self.screenshot(f"FAIL_OCR_{text_to_find.replace(' ', '_')}")
        return False

    def wait_and_click_by_template(self, template_name: str, timeout: int = 20, threshold: float = 0.8) -> bool:
        """
        Espera até que um template de imagem seja encontrado via OpenCV e clica no seu centro.
        Faz tentativas a cada 1 segundo.
        """
        template_path = TEMPLATE_DIR / template_name
        if not template_path.exists():
            print(f"Template {template_name} não encontrado no diretório {TEMPLATE_DIR}")
            return False

        start_time = time.time()
        while time.time() - start_time < timeout:
            current_screen_path = self.screenshot('wait_template_temp')
            x, y = template_match_location(current_screen_path, str(template_path), threshold)
            
            if x is not None:
                self.click_xy(x, y)
                self.screenshot(f"click_template_{template_name.replace('.', '_')}")
                print(f"✅ Template Clicado em '{template_name}'")
                return True
            
            time.sleep(1)
        
        print(f"❌ ERRO: Template '{template_name}' não encontrado via OpenCV após {timeout}s.")
        self.screenshot(f"FAIL_TEMPLATE_{template_name.replace('.', '_')}")
        return False