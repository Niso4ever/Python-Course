"""
═══════════════════════════════════════════════════════════════════
LESSON 8 CHEATSHEET: Import Deep Dive
═══════════════════════════════════════════════════════════════════
Virtual environments, requirements, and package management.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. VENV COMMANDS (run in terminal, not Python)
# ═══════════════════════════════════════════════════════════
"""
CREATE:   python -m venv .venv
ACTIVATE: source .venv/bin/activate        (Mac/Linux)
          .venv\\Scripts\\activate          (Windows)
CONFIRM:  (.venv) appears in prompt
DEACTIVATE: deactivate

INSTALL:  pip install anthropic langchain-anthropic
CAPTURE:  pip freeze > requirements.txt
RESTORE:  pip install -r requirements.txt
UPGRADE:  pip install langchain-anthropic --upgrade
CHECK:    pip show langchain-anthropic     → shows version + location
LIST:     pip list                          → all installed packages
"""

# ═══════════════════════════════════════════════════════════
# 2. REQUIREMENTS.TXT — COMMON AI STACKS
# ═══════════════════════════════════════════════════════════
"""
Versions checked 2026-10-28. Pins marked (venv) match the shared AIarch
virtualenv. Pins marked (2024, unchecked) are not installed there and have
not been re-tested; look up the current version on pypi.org before using them.
LangChain 1.x needs a matching langchain-anthropic 1.x, so update both together.

STACK: Anthropic Direct
─────────────────────
anthropic==1.11.0                 (venv)
python-dotenv==1.2.4              (venv)

STACK: LangChain RAG
─────────────────────
langchain==1.2.10                 (venv)
langchain-anthropic==0.3.3        (2024, unchecked — too old for langchain 1.x)
langchain-community==0.4.1        (venv)
langchain-core==1.2.17            (venv)
langchain-text-splitters==1.1.1   (venv)
chromadb==1.5.9                   (latest on pypi.org, 2026-10-28; not in venv)
sentence-transformers==3.3.1      (2024, unchecked)
python-dotenv==1.2.4              (venv)

STACK: DSPy
─────────────────────
dspy==3.4.0                       (venv; the old name dspy-ai is now only an alias)
anthropic==1.11.0                 (venv)
python-dotenv==1.2.4              (venv)

STACK: CrewAI
─────────────────────
crewai==0.80.0                    (2024, unchecked — crewai 1.x has been out since Oct 2025)
crewai-tools==0.14.0              (2024, unchecked)
python-dotenv==1.2.4              (venv)
"""

# ═══════════════════════════════════════════════════════════
# 3. PIP → IMPORT NAME MAPPING (quick reference)
# ═══════════════════════════════════════════════════════════
"""
pip install name              import name
─────────────────────────     ─────────────────────────────
anthropic                 →   import anthropic
langchain                 →   import langchain
langchain-anthropic       →   from langchain_anthropic import ...
langchain-community       →   from langchain_community import ...
langchain-core            →   from langchain_core import ...
langchain-text-splitters  →   from langchain_text_splitters import ...
python-dotenv             →   from dotenv import load_dotenv
chromadb                  →   import chromadb
dspy                      →   import dspy        (was dspy-ai)
crewai                    →   from crewai import ...
sentence-transformers     →   from sentence_transformers import ...
faiss-cpu                 →   import faiss
"""

# ═══════════════════════════════════════════════════════════
# 4. VERSION DIAGNOSIS
# ═══════════════════════════════════════════════════════════
import importlib

def check_version(package_name: str):
    """Check installed version of any package."""
    try:
        pkg = importlib.import_module(package_name.replace("-", "_"))
        version = getattr(pkg, "__version__", "unknown")
        print(f"{package_name}: {version}")
    except ImportError:
        print(f"{package_name}: NOT INSTALLED")

# Usage:
# check_version("anthropic")
# check_version("langchain")
# check_version("chromadb")

def check_all_ai_packages():
    """Check all common AI packages at once."""
    packages = [
        "anthropic", "langchain", "langchain_anthropic",
        "langchain_community", "chromadb", "dspy", "crewai"
    ]
    print("Package Status:")
    for pkg in packages:
        check_version(pkg)

# ═══════════════════════════════════════════════════════════
# 5. SYS.PATH INSPECTION
# ═══════════════════════════════════════════════════════════
import sys

def show_python_paths():
    """See where Python looks for imports."""
    print("Python search paths (in order):")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")
    print(f"\nActive Python: {sys.executable}")

# ═══════════════════════════════════════════════════════════
# 6. FIND WHERE A PACKAGE IS INSTALLED
# ═══════════════════════════════════════════════════════════
def locate_package(package_name: str):
    """Find the physical location of an installed package."""
    try:
        pkg = importlib.import_module(package_name)
        print(f"{package_name} is at: {pkg.__file__}")
    except ImportError:
        print(f"{package_name} not found")
    except AttributeError:
        print(f"{package_name} found but has no __file__")

# ═══════════════════════════════════════════════════════════
# END
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=== Python Environment Info ===")
    show_python_paths()
    print("\n=== AI Package Status ===")
    check_all_ai_packages()
