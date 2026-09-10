import re

def validate_brand_name(value):
    if not isinstance(value, str) or not value:
        return False
    return len(value) >= 2 and len(value) <= 50

def validate_brand_color(value):
    if not isinstance(value, str):
        return False
    hex_pattern = r'^#[0-9a-fA-F]{6}$'
    colors = {'red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple'}
    return bool(re.match(hex_pattern, value)) or value.lower() in colors

def validate_brand_logo_url(value):
    if not isinstance(value, str) or not value:
        return False
    url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(url_pattern, value))