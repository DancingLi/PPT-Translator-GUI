"""Run GUI test application.

This is a simple entry point to test the GUI components.
"""

import sys
import os

# Add gui directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gui'))

# Import and run test
from test_components import main

if __name__ == '__main__':
    main()
