"""Import helper for testing without prior installation.

Allows simple imports of the pyseus package in test files without
prior installation. Usage: from context import pyseus.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../")))

import pyseus
