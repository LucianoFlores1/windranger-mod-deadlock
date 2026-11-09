import subprocess

code = """
import bpy
import os
from pathlib import Path

# Load warka3_orig and inspect right arm bones and vertices
from tools.build_restored_perfect_windrunner import build_body
"""
