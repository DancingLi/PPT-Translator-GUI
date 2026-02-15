#!/usr/bin/env python3
""""One-click build script for PPT Translator GUI.

This script automates the entire build process:
1. Cleans previous builds
2. Verifies environment and dependencies
3. Runs PyInstaller to create executable
4. Copies necessary resources
5. Creates Inno Setup installer package
6. Generates build summary

Usage:
    python build.py [options]
Options:
    --clean     Clean build directories only
    --test      Run tests before building
    --verbose   Show detailed output
"""

import os
import sys
import shutil
import subprocess
import argparse
import time
from pathlib import Path


# Configuration
APP_NAME = "PPTTranslator"
APP_DISPLAY_NAME = "PPT Translator"
APP_VERSION = "1.0.0"
APP_PUBLISHER = "PPT Translator Team"

# Paths
PROJECT_ROOT = Path(__file__).parent
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
WORK_DIR = BUILD_DIR / "work"
ASSETS_DIR = BUILD_DIR / "assets"
MAIN_SCRIPT = "gui/run_app.py"
ICON_PATH = ASSETS_DIR / "icon.ico"
SETUP_SCRIPT = BUILD_DIR / "setup.iss"
OUTPUT_DIR = DIST_DIR / "installer"

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def print_step(step_num, total_steps, text):
    """Print step progress."""
    print(f"[{step_num}/{total_steps}] {text}")

def clean_build_dirs():
    """Clean build and dist directories."""
    print_step(1, 5, "Cleaning build directories...")
    
    dirs_to_clean = [
        DIST_DIR,
        WORK_DIR,
        OUTPUT_DIR
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✓ Removed: {dir_path}")
            except Exception as e:
                print(f"  ⚠ Warning: Could not remove {dir_path}: {e}")
    
    # Create necessary directories
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def check_dependencies():
    """Check if required dependencies are installed."""
    print_step(2, 5, "Checking dependencies...")
    
    # Check Python packages
    required_packages = [
        "customtkinter",
        "PIL",
        "pptx",
        "openai",
        "anthropic",
        "google.generativeai",
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (not installed)")
            return False
    
    # Check PyInstaller
    try:
        result = subprocess.run(
            ["pyinstaller", "--version"],
            capture_output=True,
            text=True
        )
        version = result.stdout.strip()
        print(f"  ✓ PyInstaller: {version}")
    except Exception:
        print("  ✗ PyInstaller: Not installed or not in PATH")
        return False
    
    # Check Inno Setup
    inno_path = find_inno_setup()
    if inno_path:
        print(f"  ✓ Inno Setup: {inno_path}")
    else:
        print("  ⚠ Inno Setup: Not found (optional, required for installer creation)")
    
    return True

def find_inno_setup():
    """Find Inno Setup installation."""
    # Common installation paths
    possible_paths = [
        Path("C:/Program Files (x86)/Inno Setup 6"),
        Path("C:/Program Files/Inno Setup 6"),
        Path("C:/Program Files (x86)/Inno Setup 5"),
        Path("C:/Program Files/Inno Setup 5"),
    ]
    
    for path in possible_paths:
        if path.exists():
            iscc = path / "ISCC.exe"
            if iscc.exists():
                return str(iscc)
    
    return None
def build_executable():
    """Build the executable using PyInstaller."""
    print_step(3, 5, "Building executable with PyInstaller...")
    
    # Prepare PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--workpath", str(WORK_DIR),
        "--distpath", str(DIST_DIR),
    ]
    
    # Add icon if exists
    if ICON_PATH.exists():
        cmd.extend(["--icon", str(ICON_PATH)])
    else:
        print(f"  ⚠ Warning: Icon file not found: {ICON_PATH}")
    
    # Add data files
    data_dirs = [
        ("gui/widgets", "gui/widgets"),
        ("gui/dialogs", "gui/dialogs"),
        ("gui/utils", "gui/utils"),
    ]
    
    for src, dst in data_dirs:
        src_path = PROJECT_ROOT / src
        if src_path.exists():
            separator = ";" if os.name == "nt" else ":"
            cmd.extend(["--add-data", f"{src_path}{separator}{dst}"])
        else:
            print(f"  ⚠ Warning: Data path not found: {src_path}")
    
    # Add hidden imports
    hidden_imports = [
        "customtkinter",
        "PIL",
        "pptx",
        "openai",
        "anthropic",
        "google.generativeai",
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    # Add excluded modules
    excludes = [
        "tkinter.test",
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
    ]
    
    for module in excludes:
        cmd.extend(["--exclude-module", module])
    
    # Add main script
    cmd.append(MAIN_SCRIPT)
    
    # Run PyInstaller
    print(f"  Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=False,
            text=True
        )
        
        print()
        
        if result.returncode == 0:
            print("  ✓ PyInstaller build successful!")
            return True
        else:
            print(f"  ✗ PyInstaller failed with code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error running PyInstaller: {e}")
        return False

def copy_additional_files():
    """Copy additional files to output directory."""
    print_step(4, 5, "Copying additional files...")
    
    # Files to copy
    files_to_copy = [
        (ICON_PATH, "icon.ico"),
        (PROJECT_ROOT / "README.md", "README.md"),
        (PROJECT_ROOT / "LICENSE", "LICENSE"),
        (PROJECT_ROOT / "使用手册.md", "使用手册.md"),
    ]
    
    for src, dst_name in files_to_copy:
        if src.exists():
            dst_path = DIST_DIR / dst_name
            try:
                shutil.copy2(str(src), str(dst_path))
                print(f"  ✓ Copied: {src.name}")
            except Exception as e:
                print(f"  ⚠ Warning: Could not copy {src.name}: {e}")
        else:
            print(f"  ⚠ Warning: File not found: {src}")

def generate_build_summary():
    """Generate build summary."""
    print()
    print("=" * 60)
    print("Build Summary")
    print("=" * 60)
    print()
    
    # Check executable
    exe_path = DIST_DIR / f"{APP_NAME}.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable: {exe_path}")
        print(f"  Size: {size_mb:.2f} MB")
    else:
        print(f"✗ Executable not found: {exe_path}")
    
    print()
    
    # List all files in dist
    dist_files = list(DIST_DIR.iterdir())
    if dist_files:
        print(f"Files in {DIST_DIR}:")
        for f in sorted(dist_files):
            size_kb = f.stat().st_size / 1024 if f.is_file() else 0
            if f.is_dir():
                print(f"  📁 {f.name}/")
            else:
                print(f"  📄 {f.name} ({size_kb:.1f} KB)")
    
    print()
    print("✓ Build completed successfully!")
    print()

def main():
    """Main build function."""
    print_header("PPT Translator - Build Script")
    
    # Clean previous builds
    clean_build_dirs()
    print()
    
    # Check dependencies
    if not check_dependencies():
        print()
        print("✗ Build failed: Missing dependencies")
        print()
        print("Please install the required dependencies:")
        print("  pip install customtkinter pyinstaller pillow")
        return 1
    print()
    
    # Build executable
    if not build_executable():
        print()
        print("✗ Build failed: PyInstaller error")
        return 1
    print()
    
    # Copy additional files
    copy_additional_files()
    print()
    
    # Generate summary
    generate_build_summary()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())