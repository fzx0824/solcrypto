import sys
import math
from random import randint
from py_ecc import bn128
from py_ecc.bn128 import add, multiply, curve_order, G1
from py_ecc.bn128.bn128_field_elements import inv, field_modulus

from .utils import hashs, bytes_to_int, powmod

randsn = lambda: randint(1, curve_order - 1)
sbmul = lambda s: multiply(G1, s)
hashsn = lambda *x: hashs(*x) % curve_order
hashpn = lambda *x: hashsn(*[item.n for sublist in x for item in sublist])
addmodn = lambda x, y: (x + y) % curve_order
addmodp = lambda x, y: (x + y) % field_modulus
mulmodn = lambda x, y: (x * y) % curve_order
mulmodp = lambda x, y: (x * y) % field_modulus
submodn = lambda x, y: (x - y) % curve_order
invmodn = lambda x: inv(x, curve_order)
negp = lambda x: (x[0], -x[1])


def evalcurve(x):
	a = 5472060717959818805561601436314318772174077789324455915672259473661306552146
	beta = addmodp(mulmodp(mulmodp(x, x), x), 3)
	y = powmod(beta, a, field_modulus)
	return (beta, y)


def hashtopoint(x):
	assert isinstance(x, long)
	x = x % curve_order
	while True:
		beta, y = evalcurve(x)
		if beta == mulmodp(y, y):
			return x, y
		x = addmodp(x, 1)


if __name__ == "__main__":
	# Sanity test
	beta, y = evalcurve(1)
	assert mulmodp(y, y) == beta
	assert y == 2

	# Compatibility test
	from hashlib import sha256
	z = bytes_to_int(sha256('hello world').digest())
	x, y = hashtopoint(z)
	assert x == 18149469767584732552991861025120904666601524803017597654373315627649680264678L
	assert y == 18593544354303197021588991433499968191850988132424885073381608163097237734820L

	# Compatibility with: uint256(keccak256(uint256(1), uint256(2), uint256(3))) % Curve.N();
	assert hashsn(1, 2, 3) == 5999809398626971894156481321441750001229812699285374901473004231265197659290
