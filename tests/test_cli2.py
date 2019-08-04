import ptvsd

from context import pyseus

# VSC remote debugging
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()

pyseus._console_entry()
