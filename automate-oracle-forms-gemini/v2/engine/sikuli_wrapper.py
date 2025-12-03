# engine/sikuli_wrapper.py
# Wrapper to run Sikuli scripts from Python.
# Enhancements:
# - before running, generate template variants using ia/ia_visao.generate_template_variants
# - capture stdout/stderr and return code to test runner
# - configurable path to sikulix.jar

import os, subprocess, glob, shutil
from pathlib import Path

# Update this path to your local sikulix jar
SIKULI_JAR = os.environ.get('SIKULI_JAR', r'C:\sikulix\sikulix.jar')

# Import ia_visao dynamically to avoid heavy imports if not needed
def generate_variants_for_templates(sikuli_script_dir):
    \"\"\"For each PNG in templates/, generate small variants and save under templates/variants/<basename>/\"\"\"
    try:
        from ia import ia_visao
    except Exception as e:
        # If ia_visao is not available, skip silently
        print('ia_visao not available, skipping variant generation:', e)
        return
    templates_dir = Path(sikuli_script_dir) / 'templates'
    variants_root = templates_dir / 'variants'
    variants_root.mkdir(parents=True, exist_ok=True)
    for png in templates_dir.glob('*.png'):
        name = png.stem
        out_dir = variants_root / name
        if not out_dir.exists() or len(list(out_dir.glob('*.png'))) < 3:
            # only generate if not present to save time
            ia_visao.generate_template_variants(str(png), str(out_dir))

def executar_sikuli(sikuli_script_path: str, timeout: int = 600):
    sikuli_script_path = os.path.abspath(sikuli_script_path)
    # pre-generate template variants to improve Sikuli robustness
    generate_variants_for_templates(sikuli_script_path)
    cmd = ['java', '-jar', SIKULI_JAR, '-r', sikuli_script_path]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'
