# report/generate_report.py

import json
import sys
import os
from pathlib import Path
from flask import Flask, render_template_string

# Template HTML simples para o relatório executivo (usando Flask para renderizar)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório Executivo de Automação</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
        .container { max-width: 900px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .metric-box { display: flex; justify-content: space-around; margin-bottom: 20px; }
        .box { padding: 15px; border-radius: 6px; text-align: center; color: white; width: 30%; }
        .passed { background-color: #28a745; }
        .failed { background-color: #dc3545; }
        .total { background-color: #007bff; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        .status-PASSED { background-color: #d4edda; color: #155724; }
        .status-FAILED { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório Executivo de Automação</h1>
        <p><strong>Executado em:</strong> {{ timestamp }}</p>

        <div class="metric-box">
            <div class="box total">
                <h2>Total de Testes</h2>
                <p>{{ total_tests }}</p>
            </div>
            <div class="box passed">
                <h2>Sucesso (%)</h2>
                <p>{{ success_rate }}%</p>
            </div>
            <div class="box failed">
                <h2>Falhas</h2>
                <p>{{ failed_tests }}</p>
            </div>
        </div>

        <h3>Métricas de Tempo</h3>
        <ul>
            <li><strong>Tempo Total de Execução:</strong> {{ total_duration | round(2) }} segundos</li>
            <li><strong>Média por Teste:</strong> {{ avg_duration | round(2) }} segundos</li>
        </ul>

        <h3>Detalhes da Execução</h3>
        <table>
            <thead>
                <tr>
                    <th>Teste</th>
                    <th>Duração (s)</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {% for run in test_runs %}
                <tr class="status-{{ run.status }}">
                    <td>{{ run.name }}</td>
                    <td>{{ run.duration | round(2) }}</td>
                    <td>{{ run.status }}</td>
                    <td>{{ run.timestamp }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <p style="margin-top: 30px;">Relatório detalhado disponível no Allure: <code>allure serve reports/allure</code></p>
    </div>
</body>
</html>
"""

app = Flask(__name__)

def generate_report(metrics_path, output_html_path):
    """Lê o JSON de métricas e gera o relatório HTML."""
    try:
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)['test_runs']
    except FileNotFoundError:
        print(f"Erro: Arquivo de métricas não encontrado em {metrics_path}")
        return
    except json.JSONDecodeError:
        print(f"Erro: Arquivo de métricas inválido (JSON) em {metrics_path}")
        return

    total_tests = len(metrics)
    passed_tests = sum(1 for m in metrics if m['status'] == 'PASSED')
    failed_tests = total_tests - passed_tests
    total_duration = sum(m['duration'] for m in metrics)
    avg_duration = total_duration / total_tests if total_tests > 0 else 0
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    context = {
        'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'total_duration': total_duration,
        'avg_duration': avg_duration,
        'success_rate': success_rate,
        'test_runs': metrics
    }

    # Renderiza o template HTML usando Flask
    with app.app_context():
        html_content = render_template_string(HTML_TEMPLATE, **context)

    # Salva o arquivo HTML
    Path(output_html_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Relatório executivo gerado com sucesso em: {output_html_path}")


if __name__ == '__main__':
    # Uso CLI: python report/generate_report.py reports/metrics.json reports/summary.html
    if len(sys.argv) != 3:
        print("Uso: python generate_report.py <caminho_metrics_json> <caminho_output_html>")
        sys.exit(1)

    metrics_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_report(metrics_file, output_file)