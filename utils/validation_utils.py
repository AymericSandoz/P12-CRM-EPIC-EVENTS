# utils/validation_utils.py

import re
import phonenumbers


def validate_email(email):
    """Validate if the email address is correct."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def validate_employee_number(employee_number):
    """Validate if the employee number is a valid number."""
    return employee_number.isdigit()


def validate_phone_number(phone_number):
    """Validate a phone number using the phonenumbers library."""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
