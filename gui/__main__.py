"""Main entry point for GUI module.

This module can be run directly: python -m gui
"""

import sys
import os

# Ensure the package can be imported
if __name__ == '__main__':
    # Add parent directory to path for relative imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from gui.test_components import main
    main()
