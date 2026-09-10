def validate_chp_id(value):
    if not isinstance(value, str):
        return False
    return value.startswith('CHP') and len(value) == 6 and value[3:].isdigit()

def validate_household_id(value):
    if not isinstance(value, str) or not value:
        return False
    return value.startswith('HH') and len(value) == 5 and value[2:].isdigit()

def validate_referral_status(value):
    if not isinstance(value, str):
        return False
    return value in ('pending', 'resolved')