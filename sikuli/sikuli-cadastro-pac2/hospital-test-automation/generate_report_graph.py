import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os

def parse_surefire_report(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    test_suite_name = root.get('name')
    tests = int(root.get('tests', 0))
    failures = int(root.get('failures', 0))
    errors = int(root.get('errors', 0))
    skipped = int(root.get('skipped', 0))
    time = float(root.get('time', 0.0))

    return {
        'TestSuite': test_suite_name,
        'Tests': tests,
        'Failures': failures,
        'Errors': errors,
        'Skipped': skipped,
        'Time (s)': time
    }

def generate_graph(metrics_df, output_dir="./reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 7))

    metrics_df[['Tests', 'Failures', 'Errors', 'Skipped']].plot(kind='bar', ax=ax, colormap='viridis')

    ax.set_title('Métricas de Teste por Test Suite')
    ax.set_ylabel('Contagem')
    ax.set_xlabel('Test Suite')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    graph_path = os.path.join(output_dir, 'test_metrics_graph.png')
    plt.savefig(graph_path)
    print(f"Gráfico de métricas salvo em: {graph_path}")
    return graph_path

if __name__ == '__main__':
    reports_dir = './target/surefire-reports'
    all_metrics = []

    for filename in os.listdir(reports_dir):
        if filename.startswith('TEST-') and filename.endswith('.xml'):
            file_path = os.path.join(reports_dir, filename)
            metrics = parse_surefire_report(file_path)
            all_metrics.append(metrics)

    if all_metrics:
        metrics_df = pd.DataFrame(all_metrics)
        print("Métricas de Teste Coletadas:")
        print(metrics_df)
        graph_file = generate_graph(metrics_df)
    else:
        print("Nenhum relatório Surefire XML encontrado.")

