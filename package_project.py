import os
import zipfile
import shutil

ROOT_DIR = os.path.abspath(".")
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
DIST_DIR = os.path.join(ROOT_DIR, "dist")
os.makedirs(PUBLIC_DIR, exist_ok=True)

# 1. Package Complete Source Code (with GitHub Actions deploy workflow)
source_zip_path = os.path.join(PUBLIC_DIR, "aurelia-website-source.zip")
exclude_dirs = {"node_modules", ".git", "dist", "__pycache__"}
exclude_extensions = {".zip", ".tar.gz", ".pyc"}

with zipfile.ZipFile(source_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in exclude_extensions and file != "deploy.yml":
                continue
            if file == "package_project.py":
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            zf.write(full_path, rel_path)

print(f"Created source zip: {source_zip_path} ({os.path.getsize(source_zip_path)} bytes)")

# Copy source zip to other aliases so older links continue to work
shutil.copyfile(source_zip_path, os.path.join(PUBLIC_DIR, "aurelia-src.zip"))
shutil.copyfile(source_zip_path, os.path.join(PUBLIC_DIR, "website-files.zip"))

# 2. Package Pre-Built Ready-To-Deploy Static HTML/JS/CSS (dist)
# This lets the user just drop into GitHub Pages without any build commands!
deploy_ready_zip_path = os.path.join(PUBLIC_DIR, "aurelia-website-deploy-ready.zip")
with zipfile.ZipFile(deploy_ready_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(DIST_DIR):
        for file in files:
            if file.endswith(".zip") or file.endswith(".tar.gz"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, DIST_DIR)
            zf.write(full_path, rel_path)

print(f"Created deploy-ready zip: {deploy_ready_zip_path} ({os.path.getsize(deploy_ready_zip_path)} bytes)")

# Also copy both zip files to dist so server serves them directly in production if static
shutil.copyfile(source_zip_path, os.path.join(DIST_DIR, "aurelia-website-source.zip"))
shutil.copyfile(source_zip_path, os.path.join(DIST_DIR, "aurelia-src.zip"))
shutil.copyfile(source_zip_path, os.path.join(DIST_DIR, "website-files.zip"))
shutil.copyfile(deploy_ready_zip_path, os.path.join(DIST_DIR, "aurelia-website-deploy-ready.zip"))
print("Done packaging!")
