import re

class InputValidator:
    
    @staticmethod
    def validate_name(name):
        name = name.strip()
        if not name:
            return (False, "Name cannot be empty")
        
        if len(name) < 2:
            return (False, "Name is too short")
            
        if not all(c.isalpha() or c.isspace() or c in ".-'" for c in name):
            return (False, "Name contains invalid characters")
            
        return (True, "")
    
    @staticmethod
    def validate_phone(phone):
        phone = phone.strip()
        if not phone:
            return (False, "Phone number cannot be empty")
        
        cleaned_phone = re.sub(r'[\s\-\(\)\.]+', '', phone)
        
        if not cleaned_phone.isdigit():
            return (False, "Phone number should contain only digits, spaces, and common separators")
            
        if len(cleaned_phone) < 10:
            return (False, "Phone number is too short")
            
        return (True, "")
    
    @staticmethod
    def validate_email(email):
        email = email.strip()
        if not email:
            return (False, "Email cannot be empty")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return (False, "Invalid email format")
            
        return (True, "")
        
    @staticmethod
    def validate_appointment_form(name, phone, email):
        errors = []
        
        name_valid, name_error = InputValidator.validate_name(name)
        if not name_valid:
            errors.append(name_error)
            
        phone_valid, phone_error = InputValidator.validate_phone(phone)
        if not phone_valid:
            errors.append(phone_error)
            
        email_valid, email_error = InputValidator.validate_email(email)
        if not email_valid:
            errors.append(email_error)
            
        return (len(errors) == 0, errors)