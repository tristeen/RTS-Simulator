import logging
import logging.handlers
import config

x = logging.getLogger("logfun")
x.setLevel(logging.INFO)
#x.setLevel(logging.DEBUG)

h1 = logging.FileHandler("mRTS.log")
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d: %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)

h = logging.StreamHandler()
f = logging.Formatter("%(levelname)s %(asctime)s: %(message)s")
h.setFormatter(f)
h.setLevel(logging.INFO)
x.addHandler(h)

class A(object):

	def __getattr__(self, name):
		return self

	def __call__(self, *args, **kwargs):
		return self

if config.log:
	log = logging.getLogger("logfun")
else:
	log = A()
