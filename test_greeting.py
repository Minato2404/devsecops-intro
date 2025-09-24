import sys
import os
sys.path.append(os.path.dirname(__file__))

from greeting import greeting

def test_greeting():
    assert greeting("Polibest") == "Hello Polibest, welcome to DevSecOps!"

