import os
import argparse
from datetime import datetime

# =============================================================================
# 1. STRATEGIC CONFIGURATION (THE FOUNDATION)
# =============================================================================

DEFAULT_DEPTH = 4
DEFAULT_MODE = "ai"

# The Absolute Whitelist: If it's not here, it doesn't exist.
FILE_EXTENSIONS_TO_INCLUDE = (
    '.py', '.ipynb', '.sql', '.js', '.ts', '.html', '.css', # Code
    '.md', '.txt', '.pdf',                                  # Docs
    '.csv', '.xlsx', '.json', '.db', '.sqlite',             # Data
    '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env',       # Config
    'requirements.txt', 'Dockerfile', 'docker-compose.yml', # Project
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'        # Images
)

# The Assassination List (Global File Exclusions)
NOISE_FILES = {'__init__.py'}

# Directory Exclusions (os.walk will not enter these)
DIRECTORIES_TO_EXCLUDE = {
    '.git', '__pycache__', 'venv', 'conda', 'node_modules',
    '.sf', '.sfdx', '.vscode', '.idea', 'build', 'dist', 'logs',
    '.egg-info', '_inbox', '_archives', '_img', '_prompts'
}

# Categories for Truncation Overlays
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
CODE_EXTENSIONS = ('.py', '.ipynb', '.sql', '.js', '.ts', '.html', '.css')

# =============================================================================
# 2. THE CRYSTAL MODE IMMUNITY LOGIC
# =============================================================================

def is_immune_zone(current_path: str, filename: str) -> bool:
    """Evaluates if a code file is in a structural zone and should bypass the 2-file cap."""
    norm_path = os.path.normpath(current_path)
    path_parts = norm_path.split(os.sep)

    # 1. src/acn/
    if 'src' in path_parts and 'acn' in path_parts:
        if path_parts.index('acn') == path_parts.index('src') + 1:
            return True
            
    # 2. src/aaicore/
    if 'src' in path_parts and 'aaicore' in path_parts:
        if path_parts.index('aaicore') == path_parts.index('src') + 1:
            return True

    # 3. reference/notebooks/
    if 'reference' in path_parts and 'notebooks' in path_parts:
        if path_parts.index('notebooks') == path_parts.index('reference') + 1:
            return True

    # 4. Any .ipynb inside main/
    if filename.endswith('.ipynb') and 'main' in path_parts:
        return True
        
    return False

# =============================================================================
# 3. THE CORE MAP GENERATOR
# =============================================================================

def generate_consolidated_lde(target_dirs: list, max_depth: int, mode: str, output_file: str):
    print(f"[*] FORGING CONSOLIDATED LDE MAP")
    print(f"[*] Mode: {mode.upper()} | Max Depth: {max_depth}")
    
    total_dirs_scanned = 0
    total_files_included = 0

    with open(output_file, "w", encoding="utf-8") as f:
        # --- Write Global Header ---
        f.write("=" * 80 + "\n")
        f.write(f"LDE CONSOLIDATED CONTEXT SNAPSHOT ({mode.upper()} MODE)\n")
        f.write("-" * 80 + "\n")
        f.write(f"GENERATED ON   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"MAX DEPTH      : {max_depth}\n")
        f.write("=" * 80 + "\n\n")

        # --- Process Each Target Directory ---
        for root_dir in target_dirs:
            root_dir = os.path.abspath(root_dir)
            
            if not os.path.isdir(root_dir):
                print(f"[!] Warning: Target not found, skipping -> {root_dir}")
                continue
                
            # --- NEW ADDITION: Skip if the root target itself is an Obsidian proxy ---
            if os.path.isdir(os.path.join(root_dir, '.obsidian')):
                print(f"[!] Skipping Obsidian proxy directory: {root_dir}")
                continue

            root_depth = root_dir.rstrip(os.sep).count(os.sep)
            
            f.write(f"🎯 TARGET: {os.path.basename(root_dir)} (Path: {root_dir})\n")
            f.write("-" * 80 + "\n")

            for current_path, dirnames, filenames in os.walk(root_dir, topdown=True):
                # 1. Filter Directories (Noise, Depth, and Obsidian Proxies)
                valid_dirs = []
                for d in dirnames:
                    if d in DIRECTORIES_TO_EXCLUDE:
                        continue
                    # --- NEW ADDITION: Drop any folder containing a '.obsidian' subfolder ---
                    if os.path.isdir(os.path.join(current_path, d, '.obsidian')):
                        continue
                    valid_dirs.append(d)
                
                dirnames[:] = valid_dirs
                
                current_depth = current_path.rstrip(os.sep).count(os.sep) - root_depth
                
                if current_depth >= max_depth:
                    dirnames[:] = []
                    if current_depth > max_depth:
                        continue

                # 2. Print Directory Name
                indent = "    " * current_depth
                folder_name = os.path.basename(current_path)

                if current_depth > 0:
                    f.write(f"{indent[:-4]}└── {folder_name}/\n")
                    total_dirs_scanned += 1

                # 3. Categorize and Filter Files
                file_indent = indent + "    "
                
                standard_files = []
                image_files = []
                code_files = []
                
                for filename in filenames:
                    # Apply Absolute Foundation Rules
                    if not filename.endswith(FILE_EXTENSIONS_TO_INCLUDE) and filename not in FILE_EXTENSIONS_TO_INCLUDE:
                        continue
                    if filename in NOISE_FILES:
                        continue
                        
                    # Categorize for Truncation Overlays
                    if filename.lower().endswith(IMAGE_EXTENSIONS):
                        image_files.append(filename)
                    elif filename.endswith(CODE_EXTENSIONS):
                        code_files.append(filename)
                    else:
                        standard_files.append(filename)

                # 4. Apply Truncation Rules
                files_to_print = standard_files.copy()
                hidden_image_count = 0
                hidden_code_count = 0
                
                # Rule A: Images (Max 5, Always on)
                image_files.sort()
                files_to_print.extend(image_files[:5])
                if len(image_files) > 5:
                    hidden_image_count = len(image_files) - 5
                    
                # Rule B: Code (Max 2, Crystal Mode Only)
                code_files.sort()
                if mode == 'crystal':
                    vulnerable_code = []
                    for code_file in code_files:
                        if is_immune_zone(current_path, code_file):
                            files_to_print.append(code_file)
                        else:
                            vulnerable_code.append(code_file)
                    
                    files_to_print.extend(vulnerable_code[:2])
                    if len(vulnerable_code) > 2:
                        hidden_code_count = len(vulnerable_code) - 2
                else:
                    # In AI mode, all code files print
                    files_to_print.extend(code_files)

                # 5. Print Files and Truncation Markers
                files_to_print.sort() # Sort everything alphabetically for aesthetics
                
                for filename in files_to_print:
                    f.write(f"{file_indent}├── {filename}\n")
                    total_files_included += 1

                if hidden_image_count > 0:
                    f.write(f"{file_indent}├── ... [{hidden_image_count} more image files hidden] ...\n")
                if hidden_code_count > 0:
                    f.write(f"{file_indent}├── ... [{hidden_code_count} more code files hidden by Crystal Mode] ...\n")

            f.write("\n") # Blank line between target directories

        # --- Write Global Footer ---
        f.write("=" * 80 + "\n")
        f.write(f"SUMMARY: Scanned {total_dirs_scanned} sub-directories and mapped {total_files_included} files.\n")
        f.write("=" * 80 + "\n")

    print(f"✅ Map successfully forged: {output_file}")
    print(f"📊 Mapped {total_files_included} files across {total_dirs_scanned} sub-directories.")


if __name__ == "__main__":
    
    help_epilog = """
----------------------------------------------------------------------
CHEAT SHEET & EXAMPLES:
----------------------------------------------------------------------
1. Default run: Automatically maps all valid subfolders in current dir (AI mode, depth 4)
   > python script_lde.py

2. Target specific folders:
   > python script_lde.py --dir "01-Master" "02-Application"

3. Run in Crystal mode (Caps code at 2 files per folder, ignores immune zones):
   > python script_lde.py --mode crystal

4. Target a specific folder, in Crystal mode, going 6 folders deep:
   > python script_lde.py --dir "axiom-ani-03-echo" --mode crystal --depth 6
----------------------------------------------------------------------
    """
    
    parser = argparse.ArgumentParser(
        description="Axiom LDE Map Generator - Builds structured context maps.",
        epilog=help_epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--dir",
        nargs='+',
        default=None, # Set to None to trigger the dynamic target logic
        help="Specific directories to scan. Defaults to all valid sub-directories in the current folder."
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=DEFAULT_DEPTH,
        help=f"Maximum depth of subdirectories to scan (default: {DEFAULT_DEPTH})."
    )
    parser.add_argument(
        "--mode",
        choices=['ai', 'crystal'],
        default=DEFAULT_MODE,
        help="Mode of operation (default: ai)."
    )
    
    args = parser.parse_args()

    try:
        # 1. Dynamic Target Logic
        if args.dir is None:
            targets = [d for d in os.listdir('.') if os.path.isdir(d) and d not in DIRECTORIES_TO_EXCLUDE]
            if not targets:
                targets = ['.']
        else:
            targets = args.dir

        # 2. Dynamic Naming Logic (Based on the folder you run the script from)
        current_dir = os.path.abspath('.')
        root_name = os.path.basename(current_dir.rstrip(os.sep))
        
        if not root_name:
            root_name = "current_dir"
            
        # I added the mode to the filename so AI and Crystal maps don't overwrite each other
        output_file = os.path.join(current_dir, f"LDE-{root_name}-{args.mode}-v1.0.txt")

        # 3. Execute
        generate_consolidated_lde(targets, args.depth, args.mode, output_file)
        
    except Exception as e:
        print(f"[!] A catastrophic error occurred: {e}")