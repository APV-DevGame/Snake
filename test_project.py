from project import set_text, center_output, set_title
from pyfiglet import Figlet

def test_set_text():
    assert set_text("hola") == set_text("hola")

def test_center_output():
    assert center_output("hola") == center_output("hola")

def test_set_title():
    assert set_title("hola") == center_output(set_text("hola"))