"""Build the reviewed second University of Wroclaw curriculum batch from local evidence.
Optional --extract fills missing PDF cell evidence before rebuilding the records.
"""
import runpy,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'docs/research/curricula/uwr-b'
sys.path.insert(0,str(root))
if '--extract' in sys.argv:
 runpy.run_path(str(root/'repair.py'),run_name='__main__')
 runpy.run_path(str(root/'supplement.py'),run_name='__main__')
runpy.run_path(str(root/'build.py'),run_name='__main__')
