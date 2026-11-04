"""Load the one owned policy before child-process imports."""
import importlib
importlib.import_module('quality_guard')
