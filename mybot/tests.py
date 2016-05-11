
def test_my_method():
	assert 12 == my_method(3, 4), "3 * 4"

def my_method(aa,bb):
	"""
	Returns aa * bb

	>>> my_method(8, 2)
	16
	>>> my_method(10, 3)
	30
	>>> my_method(13, 12)
	156
	
	"""
	return aa*bb
