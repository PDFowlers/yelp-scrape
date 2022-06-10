
from cgi import test


def hash_test(test_input: str) ->str:
    hash_value: int = hash(test_input)
    hex_str: str = hex(hash_value)
    return hex_str 

def hash_assertion(a, b):
    print(hash_test(a))
    print(hash_test(b))
    assert(hash_test(a) == hash_test(b))


print(hash_assertion('test', 'test'))
print(hash_assertion('test', 'test'))