"""
Configuration file for LLM IP Piracy framework.
Contains all path configurations to make the code portable.
"""

import os

# Auto-detect repository root (parent of src/ directory)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===== Dataset Paths =====
DATASET_PATH = os.path.join(REPO_ROOT, "all_GNN4IP_files", "IP-Netlist-toy")

# ===== GNN4IP Detection Tool Paths =====
GNN4IP_SCRIPT = os.path.join(
    REPO_ROOT, "all_GNN4IP_files", "utils", "hw2vec", 
    "examples", "use_case_3_testing_for_LLM.py"
)
GNN4IP_YAML = os.path.join(
    REPO_ROOT, "all_GNN4IP_files", "utils", "hw2vec", 
    "examples", "example_gnn4ip.yaml"
)
GNN4IP_MODEL = os.path.join(
    REPO_ROOT, "all_GNN4IP_files", "utils", "hw2vec", 
    "assets", "pretrained_DFG_IP_Netlist_toy"
)

# ===== SIM Detection Tool Paths =====
SIM_DIR = os.path.join(REPO_ROOT, "sim")
V2C_EXECUTABLE = os.path.join(SIM_DIR, "v2c")

def get_sim_executable(lang):
    """Get the path to a specific SIM language executable."""
    return os.path.join(SIM_DIR, lang)

# ===== JPlag Detection Tool Path =====
JPLAG_JAR = os.path.join(REPO_ROOT, "jplag-5.0.0-jar-with-dependencies.jar")

# ===== ABC Synthesis Tool & NanGate Libraries =====
# ABC executable and NanGate library files (now included in repository)
ABC_DIR = os.path.join(REPO_ROOT, "abc")
ABC_EXECUTABLE = os.path.join(ABC_DIR, "abc")
NANGATE_LIB = os.path.join(ABC_DIR, "NangateOpenCellLibrary_typical.lib")
NANGATE_LIB_REDUCED = os.path.join(ABC_DIR, "NangateOpenCellLibrary_typical_reduced.lib")

# ===== Output Directories =====
OUTPUT_DIR = os.path.join(REPO_ROOT, "src", "outputs")
TMP_DIR = os.path.join(REPO_ROOT, "src", "tmp")

# ===== Validation Functions =====
def validate_paths():
    """Validate that required paths exist."""
    errors = []
    
    # Check internal paths
    if not os.path.exists(DATASET_PATH):
        errors.append(f"Dataset path not found: {DATASET_PATH}")
    if not os.path.exists(GNN4IP_SCRIPT):
        errors.append(f"GNN4IP script not found: {GNN4IP_SCRIPT}")
    if not os.path.exists(GNN4IP_YAML):
        errors.append(f"GNN4IP YAML not found: {GNN4IP_YAML}")
    if not os.path.exists(GNN4IP_MODEL):
        errors.append(f"GNN4IP model not found: {GNN4IP_MODEL}")
    if not os.path.exists(V2C_EXECUTABLE):
        errors.append(f"SIM v2c not found: {V2C_EXECUTABLE}")
    if not os.path.exists(JPLAG_JAR):
        errors.append(f"JPlag JAR not found: {JPLAG_JAR}")
    if not os.path.exists(ABC_EXECUTABLE):
        errors.append(f"ABC executable not found: {ABC_EXECUTABLE}")
    if not os.path.exists(NANGATE_LIB):
        errors.append(f"NanGate library not found: {NANGATE_LIB}")
    if not os.path.exists(NANGATE_LIB_REDUCED):
        errors.append(f"NanGate reduced library not found: {NANGATE_LIB_REDUCED}")
    
    if errors:
        print("\n⚠️  Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        raise FileNotFoundError("Required files not found. Check repository structure.")
    
    print("✓ All required paths validated successfully")

if __name__ == "__main__":
    print("Repository Root:", REPO_ROOT)
    print("\nValidating paths...")
    try:
        validate_paths()
    except FileNotFoundError as e:
        print(f"\n❌ Validation failed: {e}")
