import pytest
from pkg.password.pwd import Password

def test_password():
    for i in range(10):
        password = Password.generate()
        hashed_password = Password.hash(password)
        assert Password.verify(hashed_password, password)