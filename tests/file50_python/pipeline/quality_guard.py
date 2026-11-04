"""Block network before collection and prevent dotenv files from being read."""
import json,sys
from pathlib import Path
from unittest.mock import patch

def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):raise AssertionError('External network is unavailable in reviewed contracts')
sys.addaudithook(offline)
patches=[]
def pytest_configure(config):
    scope=json.loads(Path(__file__).with_name('quality_scope.json').read_text())
    if 'offline_guard' not in scope['plugins']:
        try:
            p=patch('dotenv.load_dotenv',return_value=False);p.start();patches.append(p)
        except ImportError:pass

def pytest_unconfigure(config):
    for p in reversed(patches):p.stop()
