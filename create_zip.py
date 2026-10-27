"""
Project Packaging Script: Generates Final Distribution ZIP
==========================================================
Developer: Ms. Taniya Mondal, B.Tech
Version: 1.0

Packages all source code, models, datasets, figures, scripts, and
clinical documentation into a clean, distributable ZIP archive.
"""

import os
import zipfile

ZIP_OUTPUT_NAME = "HRV_Mental_Health_DigitalTwin_v1.0.zip"

INCLUDED_ITEMS = [
    "hrv_mwl_30.csv",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "run_dashboard.bat",
    "run_dashboard.ps1",
    "train_and_evaluate.py",
    "generate_docs.py",
    "create_zip.py",
    "WHO_HRV_DigitalTwin_Documentation.docx",
    "twin_core",
    "web_app",
    "models",
    "figures"
]

EXCLUDED_EXTENSIONS = [".pyc", ".pyo", ".git"]
EXCLUDED_DIRS = ["__pycache__", ".git"]


def package_project():
    print(f"Creating project distribution archive: {ZIP_OUTPUT_NAME}...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, ZIP_OUTPUT_NAME)
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in INCLUDED_ITEMS:
            item_path = os.path.join(base_dir, item)
            if not os.path.exists(item_path):
                print(f"  [Warning] Item not found: {item}")
                continue
                
            if os.path.isfile(item_path):
                zipf.write(item_path, arcname=item)
                print(f"  Added file: {item}")
            elif os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    # Filter out unwanted directories
                    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
                    for file in files:
                        if any(file.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
                            continue
                        full_p = os.path.join(root, file)
                        rel_p = os.path.relpath(full_p, base_dir)
                        zipf.write(full_p, arcname=rel_p)
                        print(f"  Added: {rel_p}")
                        
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\nZIP Archive successfully created: {ZIP_OUTPUT_NAME} ({size_mb:.2f} MB)")
    return zip_path


if __name__ == "__main__":
    package_project()
