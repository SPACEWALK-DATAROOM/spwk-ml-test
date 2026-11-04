"""Network remains closed in Python child processes (including Sphinx)."""
import sys
def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):raise RuntimeError('Network is closed in local quality execution')
sys.addaudithook(offline)
