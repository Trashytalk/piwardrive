import os

def check_structure():
    required_files = [
        'calibration_config.json',
        'main_localization.py',
        'logger.py',
        'requirements.txt',
        'README.md',
        'CALIBRATION.md'
    ]

    required_dirs = [
        'kismet_logs',
        'output',
        'logs'
    ]

    missing_files = [f for f in required_files if not os.path.isfile(f)]
    missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]

    if not missing_files and not missing_dirs:
        print("[✓] Project structure is complete.")
    else:
        if missing_files:
            print("[!] Missing files:")
            for f in missing_files:
                print(f"  - {f}")
        if missing_dirs:
            print("[!] Missing directories:")
            for d in missing_dirs:
                print(f"  - {d}")

if __name__ == '__main__':
    check_structure()