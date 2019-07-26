import ptvsd
from sys import stdin

from context import pyseus

# VSC remote debugging
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()
breakpoint()

pyseus._console_entry()
