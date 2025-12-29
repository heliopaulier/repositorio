import json
from datetime import datetime
from core.config import EXEC_REPORT_DIR

class Metrics:
    def __init__(self):
        self.data = {
            "timestamp": str(datetime.now()),
            "steps": [],
            "success": True
        }

    def add_step(self, name, status, duration):
        self.data["steps"].append({
            "step": name,
            "status": status,
            "duration": round(duration, 2)
        })
        if status == "FAIL":
            self.data["success"] = False

    def save(self):
        EXEC_REPORT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXEC_REPORT_DIR / "data.json", "w") as f:
            json.dump(self.data, f, indent=4)
