import sys
import os

print("🔍 PythonPath:")
for p in sys.path:
    print("  ", p)

print("\n📂 Verificando pastas e __init__:")

folders = ["engine", "vision", "tests"]

base = os.path.dirname(os.path.abspath(__file__))

for folder in folders:
    init_path = os.path.join(base, folder, "__init__.py")
    print(f"{folder}: {'OK' if os.path.exists(init_path) else 'FALTA __init__.py'}")

try:
    from engine import engine
    print("\n✅ Import engine OK")
except Exception as e:
    print("\n❌ Falha import engine:", e)
