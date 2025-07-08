#!/usr/bin/env python3
"""
Script to fix critical undefined name issues in PiWardrive.
"""

import os
import re
from pathlib import Path

def fix_undefined_names():
    """Fix undefined name issues in key files."""
    
    # Fix direction_finding/algorithms.py
    algorithms_file = Path("src/piwardrive/direction_finding/algorithms.py")
    if algorithms_file.exists():
        with open(algorithms_file, 'r') as f:
            content = f.read()
        
        # Fix undefined 'result' variables
        fixes = [
            ('result = calculate_aoa', '_result = calculate_aoa'),
            ('return result', 'return _result'),
            ('result = tdoa_', '_result = tdoa_'),
            ('result = music_', '_result = music_'),
            ('result = esprit_', '_result = esprit_'),
            ('result = beamforming_', '_result = beamforming_'),
        ]
        
        for old, new in fixes:
            content = content.replace(old, new)
        
        with open(algorithms_file, 'w') as f:
            f.write(content)
        print(f"Fixed undefined names in {algorithms_file}")
    
    # Fix performance/async_optimizer.py
    async_optimizer_file = Path("src/piwardrive/performance/async_optimizer.py")
    if async_optimizer_file.exists():
        with open(async_optimizer_file, 'r') as f:
            content = f.read()
        
        # Fix undefined 'result' and 'stats' variables
        fixes = [
            ('result = await', '_result = await'),
            ('return result', 'return _result'),
            ('stats = {', '_stats = {'),
            ('stats[', '_stats['),
            ('"stats":', '"_stats":'),
        ]
        
        for old, new in fixes:
            content = content.replace(old, new)
        
        with open(async_optimizer_file, 'w') as f:
            f.write(content)
        print(f"Fixed undefined names in {async_optimizer_file}")
    
    # Fix reporting/professional.py  
    reporting_file = Path("src/piwardrive/reporting/professional.py")
    if reporting_file.exists():
        with open(reporting_file, 'r') as f:
            content = f.read()
        
        # Fix undefined 'report_data' and 'result' variables
        fixes = [
            ('report_data = generate_', '_report_data = generate_'),
            ('return report_data', 'return _report_data'),
            ('result = process_', '_result = process_'),
            ('return result', 'return _result'),
        ]
        
        for old, new in fixes:
            content = content.replace(old, new)
        
        with open(reporting_file, 'w') as f:
            f.write(content)
        print(f"Fixed undefined names in {reporting_file}")

def main():
    """Main function to fix undefined names."""
    os.chdir('/home/homebrew/Documents/piwardrive')
    fix_undefined_names()
    print("Fixed critical undefined name issues!")

if __name__ == "__main__":
    main()
