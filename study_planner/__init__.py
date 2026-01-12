"""
Public interface definition for this module.

This module explicitly controls what symbols are exposed when
`from module import *` is used. By defining `__all__`, we prevent
accidental leakage of internal helpers or implementation details
and make the module’s intended public API clear.
"""

# __all__ exists to clearly declare the public API of this module.
# This is especially important in larger systems where modules
# contain both public entry points and internal helper functions.
__all__ = ["main"]
