import sys
import os

print("--- System Diagnostic Check ---")

# 1. Check Python Version
print(f"Python Version: {sys.version.split()[0]}")

# 2. Check Virtual Environment
venv = os.environ.get('VIRTUAL_ENV')
print(f"Virtual Environment: {venv if venv else 'NOT DETECTED'}")

# 3. Check Dependencies
required_packages = ['google-adk', 'python-dotenv']
for pkg in required_packages:
    try:
        __import__(pkg.replace('-', '_'))
        print(f"Package '{pkg}': OK")
    except ImportError:
        print(f"Package '{pkg}': MISSING")

# 4. Check Agent Initialization
try:
    from google.adk.agents import LlmAgent
    agent = LlmAgent(name="test", model="gemini-2.5-flash")
    print("Agent Initialization: SUCCESS")
except Exception as e:
    print(f"Agent Initialization: FAILED ({e})")