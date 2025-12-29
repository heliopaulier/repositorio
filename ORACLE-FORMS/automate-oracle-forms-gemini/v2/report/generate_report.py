# report/generate_report.py
# Generates executive HTML report and optionally sends an alert email if pass rate < threshold.

import json, sys, smtplib
from pathlib import Path
from email.message import EmailMessage

INPUT = sys.argv[1] if len(sys.argv)>1 else 'reports/metrics.json'
OUTPUT = sys.argv[2] if len(sys.argv)>2 else 'reports/summary.html'
EMAIL_THRESHOLD = float(sys.argv[3]) if len(sys.argv)>3 else 0.95  # e.g., 0.95

lines = Path(INPUT).read_text().strip().splitlines() if Path(INPUT).exists() else []
records = [json.loads(l) for l in lines]

total = len(records)
passed = sum(1 for r in records if r.get('status')==1)
failed = total - passed
avg_time = sum(r.get('duration',0) for r in records)/total if total>0 else 0
pass_rate = (passed/total) if total>0 else 0

html = f\"\"\"<html><head><meta charset='utf-8'><title>Relatório Executivo</title></head><body>
<h1>Resumo</h1><p>Total: {total}</p><p>Sucesso: {passed}</p><p>Falha: {failed}</p><p>Tempo médio: {avg_time:.2f}s</p><p>Taxa de sucesso: {pass_rate:.2%}</p>
</body></html>\"\"\"

Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
Path(OUTPUT).write_text(html, encoding='utf-8')
print('Gerado', OUTPUT)

# if below threshold -> send email (configure SMTP via environment variables)
if pass_rate < EMAIL_THRESHOLD:
    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASS = os.environ.get('SMTP_PASS')
    ALERT_TO = os.environ.get('ALERT_TO')  # comma-separated addresses
    if SMTP_HOST and SMTP_USER and SMTP_PASS and ALERT_TO:
        msg = EmailMessage()
        msg['Subject'] = f'[ALERTA] Testes automatizados - taxa de sucesso {pass_rate:.2%} abaixo de {EMAIL_THRESHOLD:.2%}'
        msg['From'] = SMTP_USER
        msg['To'] = ALERT_TO
        msg.set_content(f'Ver relatório: {OUTPUT}\\nSucesso: {passed}\\nFalha: {failed}\\nTaxa: {pass_rate:.2%}')
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print('Email de alerta enviado para', ALERT_TO)
    else:
        print('Parâmetros SMTP não configurados — não foi possível enviar alerta.')

