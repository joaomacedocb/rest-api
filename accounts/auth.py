from rest_framework.exceptions import APIException, AuthenticationFailed
from django.contrib.auth.hashers import check_password, make_password
import re

from accounts.models import User
from companies.models import Company, Employee


class Authentication:
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return re.match(Authentication.EMAIL_REGEX, email) is not None
        
    
    def sign_in(self, email, password) -> User:
        
        if not self.is_valid_email(email):
            raise AuthenticationFailed("Please, insert a valid e-mail.")
        
        user = User.objects.filter(email=email).first()
        
        if not user or not check_password(password, user.password):
            raise AuthenticationFailed("Invalid credentials. Please, try again.")
        
        return user
    
    def sign_up(self, name: str, email: str, password: str, type_account:str = 'owner', company_id:int = None
                ) -> User:
        
        if not all([name, email, password]):
            raise APIException("All required fields must be filled.")
        
        if not self.is_valid_email(email):
            raise APIException("Please, insert a valid e-mail.")
        
        if User.objects.filter(email=email).exists():
            raise APIException("E-mail Already registered.")
        
        if type_account == 'employee' and not company_id:
            raise APIException("Company ID cannot be null for this case.")
            
        password_hashed = make_password(password)
        
        user = User.objects.create(
            name = name,
            email = email,
            password = password_hashed,
            is_owner = type_account == 'owner',
            company_id = company_id
        )
        
        if type_account == 'owner':
            self._create_company_record(user)
        else:
            self._create_employee_record(user)
            
        return user
    
    @staticmethod
    def _create_company_record(user) -> None:
        Company.objects.create(
                name = 'Nome da empresa',
                user_id = user.id
                )
        
    @staticmethod
    def _create_employee_record(user: User, company_id: int) -> None:
            Employee.objects.create(
                company_id = company_id,
                user_id = user.id
            )