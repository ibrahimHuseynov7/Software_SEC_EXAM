import os
import re

# Folder where your group CSVs live
DATA_DIR = "/Users/ibrahimhuseynov/Big_Data_1/Software_SEC_EXAM/Data_Collection/Merged_Csv"

# Streamlit page settings
PAGE_TITLE = "Admission Recommender"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Number of recommendations to return
TOP_N = 15


def discover_group_files(data_dir: str) -> dict[int, str]:
    """
    Auto-detect group CSVs from filenames in DATA_DIR.
    Tries to extract group number from patterns like:
      merged_1ci_qrup_corrected.csv
      merged_3cu_qrup_corrected.csv
      ...anything containing '<number>' and 'qrup' and ending with .csv
    """
    if not os.path.isdir(data_dir):
        return {}

    files = [f for f in os.listdir(data_dir) if f.lower().endswith(".csv")]

    group_map: dict[int, str] = {}

    # Examples it should catch:
    # merged_1ci_qrup_corrected.csv
    # merged_2ci_qrup.csv
    # merged_3cu_qrup_corrected.csv
    # 4cu_qrup_something.csv
    patterns = [
        re.compile(r".*?(\d+)\s*(?:ci|cı|cu|cü)?\s*_?qrup.*\.csv$", re.IGNORECASE),
        re.compile(r".*?qrup.*?(\d+).*\.csv$", re.IGNORECASE),  # fallback
    ]

    for f in files:
        for pat in patterns:
            m = pat.match(f)
            if m:
                try:
                    g = int(m.group(1))
                    group_map[g] = f
                except Exception:
                    pass
                break

    return dict(sorted(group_map.items(), key=lambda x: x[0]))


GROUP_FILES = discover_group_files(DATA_DIR)

DEFAULT_GROUP = min(GROUP_FILES.keys()) if GROUP_FILES else 1
DEFAULT_CSV_PATH = (
    os.path.join(DATA_DIR, GROUP_FILES[DEFAULT_GROUP]) if GROUP_FILES else ""
)
