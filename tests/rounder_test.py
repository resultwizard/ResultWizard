def func(x):
    return x + 1


def test_answer():
    expected = 3
    expected += 2
    assert func(3) == expected
