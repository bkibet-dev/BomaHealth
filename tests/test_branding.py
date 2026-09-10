import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.branding import validate_brand_name, validate_brand_color, validate_brand_logo_url

def test_validate_brand_name_valid():
    assert validate_brand_name('BomaHealth') == True
    assert validate_brand_name('') == False
    assert validate_brand_name(None) == False

def test_validate_brand_color_valid():
    assert validate_brand_color('#FF5733') == True
    assert validate_brand_color('red') == True
    assert validate_brand_color('invalid_color') == False
    assert validate_brand_color(None) == False

def test_validate_brand_logo_url_valid():
    assert validate_brand_logo_url('https://example.com/logo.png') == True
    assert validate_brand_logo_url('invalid-url') == False
    assert validate_brand_logo_url('') == False
    assert validate_brand_logo_url(None) == False