import uvicorn
import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("================================================================================")
    print("  Q-SHIELD: Adaptive Multi-Agent Cyber-Risk & Post-Quantum Security Framework")
    print("  Starting FastAPI Core Backend on http://0.0.0.0:8000")
    print("  API Docs: http://localhost:8000/docs")
    print("================================================================================")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
