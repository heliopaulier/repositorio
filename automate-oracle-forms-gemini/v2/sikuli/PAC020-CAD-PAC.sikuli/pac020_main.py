# pac020_main.py - refactored to use helpers and robust exception handling
# Sikuli (Jython) script with detailed comments line-by-line.

import os, time, datetime, json, subprocess, shutil

# getBundlePath() is available inside Sikuli
BUNDLE = getBundlePath()
TEMPLATES = os.path.join(BUNDLE, 'templates')
GERAR_NOMES = os.path.join(BUNDLE, 'gerar-nomes')
EVIDENCE = os.path.join(BUNDLE, 'evidencia')
LOGS = os.path.join(BUNDLE, 'logs')

# Path to IA helper script (Python 3)
IA_HELPER_PY = r"C:\automacao\ia_helper.py"  # adjust to your environment

# Number of tests to run (can be set via env var QTD_TESTES)
QTD_TESTES = int(os.environ.get('QTD_TESTES', '1'))

if not os.path.exists(EVIDENCE): os.makedirs(EVIDENCE)
if not os.path.exists(LOGS): os.makedirs(LOGS)

LOG_FILE = os.path.join(LOGS, 'run.log')

# write helper functions into this script by evaluating helpers.sikuli content
# (Sikuli can execute Python code; we emulate inclusion by exec)
_helpers_code = r'''# helpers.sikuli - common helper functions for Sikuli (Jython)
# This file is meant to be imported or concatenated into Sikuli scripts.
# It provides robust click/find wrappers that try template variants and save evidence on failures.

import os, time, datetime, shutil
# FindFailed is raised by Sikuli when find() fails
# Sikuli provides the exception class in the environment
# We'll reference it directly in try/except blocks.

def safe_find_click(template_path, templates_dir=None, timeout=10):
    \"\"\"Try to find and click a template. If not found, iterate over variants in templates/variants/<basename>/*.png.
    Returns True on success, False on failure. On failure saves a screenshot evidence.\"\"\"
    try:
        # Try primary template first
        wait(template_path, timeout)
        click(template_path)
        return True
    except FindFailed:
        # primary failed — try variants folder if available
        if templates_dir is None:
            templates_dir = os.path.dirname(template_path)
        name = os.path.splitext(os.path.basename(template_path))[0]
        variants_dir = os.path.join(templates_dir, 'variants', name)
        if os.path.exists(variants_dir):
            files = sorted([os.path.join(variants_dir,f) for f in os.listdir(variants_dir) if f.lower().endswith('.png')])
            for v in files:
                try:
                    wait(v, timeout)
                    click(v)
                    return True
                except FindFailed:
                    continue
        # If we reach here, no variant matched — save evidence and rethrow
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        evid = capture(SCREEN)
        evid_dest = os.path.join(templates_dir, '..', 'evidencia', 'notfound_%s.png' % ts)
        try:
            shutil.move(evid, evid_dest)
        except:
            pass
        # log and return False (do not raise to allow graceful handling)
        print('safe_find_click: failed to find', template_path)
        return False

def safe_exists(template_path, templates_dir=None, timeout=5):
    try:
        if exists(template_path):
            return True
    except Exception:
        pass
    # try variants similarly
    if templates_dir is None:
        templates_dir = os.path.dirname(template_path)
    name = os.path.splitext(os.path.basename(template_path))[0]
    variants_dir = os.path.join(templates_dir, 'variants', name)
    if os.path.exists(variants_dir):
        for v in os.listdir(variants_dir):
            if v.lower().endswith('.png'):
                if exists(os.path.join(variants_dir, v)):
                    return True
    return False

def safe_wait(template_path, timeout=10):
    try:
        wait(template_path, timeout)
        return True
    except FindFailed:
        # try variants
        templates_dir = os.path.dirname(template_path)
        name = os.path.splitext(os.path.basename(template_path))[0]
        variants_dir = os.path.join(templates_dir, 'variants', name)
        if os.path.exists(variants_dir):
            for v in os.listdir(variants_dir):
                if v.lower().endswith('.png'):
                    try:
                        wait(os.path.join(variants_dir, v), timeout)
                        return True
                    except FindFailed:
                        continue
        return False
'''
exec(_helpers_code)

def log(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linha = "[%s] %s" % (ts, msg)
    print(linha)
    with open(LOG_FILE, 'a') as f:
        f.write(linha + '\n')

def ler_dados(path):
    # Read JSON or key=value text files into dictionary
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    dados = {}
    with open(path, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('#'): continue
            if '=' in linha:
                k,v = linha.split('=',1)
                dados[k.strip()] = v.strip()
    return dados

def chamar_ocr(img_path):
    # Call the external Python OCR helper and return its stdout (text)
    try:
        cmd = ['python', IA_HELPER_PY, 'ocr', img_path]
        out = subprocess.check_output(cmd, shell=False)
        return out.decode('utf-8').strip()
    except Exception as e:
        log('Erro OCR: %s' % e)
        return ''

def chamar_popup(img_path):
    try:
        cmd = ['python', IA_HELPER_PY, 'popup', img_path]
        out = subprocess.check_output(cmd, shell=False)
        return out.decode('utf-8').strip()
    except Exception as e:
        log('Erro popup detect: %s' % e)
        return 'NORMAL'

def salvar_evidencia(prefix='evid'):
    # capture SCREEN and move to evidencia with timestamped name
    try:
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        tmp = capture(SCREEN)
        nome = "%s_%s.png" % (prefix, ts)
        destino = os.path.join(EVIDENCE, nome)
        try:
            shutil.move(tmp, destino)
        except Exception:
            try:
                os.rename(tmp, destino)
            except Exception:
                shutil.copy(tmp, destino)
        log('Evidência salva: %s' % destino)
        return destino
    except Exception as e:
        log('Erro ao salvar evidencia: %s' % e)
        return None

def existe_popup_por_ia():
    tmp = capture(SCREEN)
    res = chamar_popup(tmp)
    return res != 'NORMAL'

def tratar_popups_comuns():
    nao_btn = os.path.join(TEMPLATES, 'cadastro-de-paciente-popup-nome-diplicado-button-click-nao.png')
    # If known popup appears, click its NO button, or attempt to detect with IA
    if safe_exists(os.path.join(TEMPLATES, 'cadastro-de-paciente-popup-nome-diplicado2.png'), TEMPLATES):
        log('Popup duplicado detectado - clicando NÃO')
        safe_find_click(os.path.join(TEMPLATES, 'cadastro-de-paciente-popup-nome-diplicado-button-click-nao.png'), TEMPLATES)
        time.sleep(1)
    if existe_popup_por_ia():
        log('Popup detectado via IA - tentando clicar NÃO se presente')
        if safe_exists(nao_btn, TEMPLATES):
            safe_find_click(nao_btn, TEMPLATES)
            time.sleep(1)

def preencher_cadastro(dados):
    # Main flow to fill patient registration using data dict
    try:
        # Validate initial screen by OCR so test can fail early if wrong app/window
        tmp0 = capture(SCREEN)
        txt0 = chamar_ocr(tmp0)
        log('OCR inicial: %s' % txt0[:120])
        if not ('Paciente' in txt0 or 'Cadastro' in txt0):
            popup('Tela inicial não confirmada via OCR. Verifique.')
            return False

        # Start search -> open registration
        if not safe_find_click(os.path.join(TEMPLATES, 'tela-inicial-busca-paciente.png'), TEMPLATES):
            salvar_evidencia('not_found_tela_inicial')
            return False
        safe_find_click(os.path.join(TEMPLATES, 'area-de-texto-busca.png'), TEMPLATES)
        type('teste')
        safe_find_click(os.path.join(TEMPLATES, 'pasquisa-paciente.png'), TEMPLATES)
        if not safe_wait(os.path.join(TEMPLATES, 'tela-pac-cad.png')):
            salvar_evidencia('no_tela_pac_cad')
            return False

        # New patient
        safe_find_click(os.path.join(TEMPLATES, 'botao-novo-paciente.png'), TEMPLATES)
        waitVanish(os.path.join(TEMPLATES, 'tela-incial-cadastro-pac.png'))

        # Fill fields with robust actions
        if not safe_find_click(os.path.join(TEMPLATES, 'area-de-texto-nome-pac.png'), TEMPLATES):
            salvar_evidencia('no_nome_field'); return False
        doubleClick(os.path.join(TEMPLATES, 'area-de-texto-nome-pac.png'))
        type(dados.get('NomePaciente',''))
        type(Key.TAB)
        type('NOME SOCIAL')
        type(Key.TAB)
        type(dados.get('DataNascimento','26081978'))
        type(Key.TAB)

        tratar_popups_comuns()

        # Continue filling other fields (examples)
        safe_find_click(os.path.join(TEMPLATES, 'tela-de-cadastro-campo-hora.png'), TEMPLATES)
        type(dados.get('Hora','1900'))
        type(Key.TAB)
        type(dados.get('Sexo','FEMININO'))
        type(Key.TAB)
        type(dados.get('Nacionalidade','BRASILEIRA'))
        type(Key.TAB)
        safe_find_click(os.path.join(TEMPLATES, 'click-ok-nacionalidade.png'), TEMPLATES)

        type(dados.get('NomeMae','')); type(Key.TAB)
        if safe_exists(os.path.join(TEMPLATES, 'poup-cadastr-inf-nome-identico.png'), TEMPLATES):
            safe_find_click(os.path.join(TEMPLATES, 'poup-cadastr-inf-nome-identico-button-nao-voltar.png'), TEMPLATES)
        safe_find_click(os.path.join(TEMPLATES, 'campo-nome-do-pai.png'), TEMPLATES)
        type(dados.get('NomePai','')); type(Key.TAB)

        type(Key.TAB); type(Key.TAB)
        type(dados.get('CPF','')); type(Key.TAB)
        type('SSP'); type(Key.TAB); type('SP'); type(Key.TAB); type(dados.get('RG','121291'))

        safe_find_click(os.path.join(TEMPLATES, 'cad-pac-aba-end.png'), TEMPLATES)
        safe_find_click(os.path.join(TEMPLATES, 'aba-endereco-campo-cep.png'), TEMPLATES)
        type(dados.get('CEP','05403-900'))
        type(Key.TAB)

        safe_find_click(os.path.join(TEMPLATES, 'cad-pac-aba-comunicacao.png'), TEMPLATES)
        safe_find_click(os.path.join(TEMPLATES, 'cad-pac-aba-comunicacao-campo-prioridade.png'), TEMPLATES)
        type(dados.get('Prioridade','1')); type(Key.TAB); type(dados.get('TipoContato','CELULAR')); type(Key.TAB)
        type(dados.get('Telefone','15 98995-8564')); type(Key.TAB)
        safe_find_click(os.path.join(TEMPLATES, 'adicionar-linha-cadastro-pac-aba-cominicacao.png'), TEMPLATES)
        type('2'); type(Key.TAB); type('E-MAIL'); type(Key.TAB); type(dados.get('Email','teste@teste.com'))

        # Save
        safe_find_click(os.path.join(TEMPLATES, 'salvar-cadastro-de-paciente.png'), TEMPLATES)
        time.sleep(8)
        tmp2 = capture(SCREEN)
        msg = chamar_ocr(tmp2)
        log('OCR pós-salvar: %s' % msg[:160])
        if any(k in msg.lower() for k in ['sucesso','salvo','cadastro realizado']):
            salvar_evidencia(prefix='cadastro_ok'); return True
        if existe_popup_por_ia():
            salvar_evidencia(prefix='cadastro_popup'); return True
        salvar_evidencia(prefix='cadastro_fail'); return False

    except Exception as e:
        log('Erro preencher_cadastro: %s' % e)
        salvar_evidencia(prefix='erro')
        return False

# Main execution: iterate through generated files up to QTD_TESTES
if __name__ == '__main__':
    arquivos = sorted([p for p in os.listdir(GERAR_NOMES) if p.lower().endswith('.json') or p.lower().endswith('.txt')])
    if not arquivos:
        popup('Nenhum dado encontrado em gerar-nomes/. Gere via engine/dados_fake.py')
    total = min(len(arquivos), QTD_TESTES)
    log('Iniciando execução: %s testes' % total)
    for i in range(total):
        arquivo = os.path.join(GERAR_NOMES, arquivos[i])
        dados = ler_dados(arquivo)
        popup('Iniciando teste %s/%s\nPaciente: %s' % (i+1, total, dados.get('NomePaciente','-')))
        inicio = time.time()
        sucesso = preencher_cadastro(dados)
        dur = time.time() - inicio
        log('Teste %s -> %s (%.2fs)' % (arquivos[i], 'OK' if sucesso else 'FAIL', dur))
        with open(os.path.join(LOGS,'metrics.log'),'a') as mf:
            mf.write('%s,%s,%.2f\n' % (arquivos[i], 'OK' if sucesso else 'FAIL', dur))
    popup('Execução finalizada. Verifique logs e evidências.')
