from pathlib import Path

from invoke import run

arg = str(Path.joinpath(Path(__file__).resolve().parents[0], 'tools', 'elasticsearch' , 'bin', 'elasticsearch.bat'))
run(arg, hide=False, echo=True)