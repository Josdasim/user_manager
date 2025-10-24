from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError, SameEmailError
from src.constants import messages
from src.repositories.user_repository import UserRepository
from src.security.password_utils import verify_password, hash_password
from src.models.user_status import UserStatus


class UserService():
    
    def __init__(self, repository:UserRepository | None = None):
        self.repository = repository or UserRepository()

    def create_user(self, username:str, email:str, password:str) -> User:
        """Crea un nuevo usuario, retorna el usuario creado"""
        if not password or len(password) < 6:
            raise UserValidationError(messages.USER_INVALID_PASSWORD)
        if self._email_exists(email):
            raise UserValidationError(messages.EMAIL_ALREADY_REGISTERED)
        password_hash = hash_password(password)
        user = User(username, email, password_hash)
        self.repository.add(user)
        return user
    
    def get_user(self, username:str) -> User:
        """Obtiene un usuario por username"""
        return self.repository.get(username)
 
    def get_all_users(self) -> list[User]:
        """Obtiene todos los usuarios registrados"""
        return self.repository.get_all()
       
    def get_user_by_email(self, email: str) -> User | None:
        """Obtiene un usuario por email"""
        return self.repository.find_by_email(email)
    
    def update_username(self, current_username: str, new_username: str) -> User:
        """Actualiza el username de un usuario"""
        user = self.get_user(current_username)       
        if user.username == new_username:
            raise UserValidationError(messages.SAME_USERNAME)      
        # Verificar que el nuevo username no exista
        if self.repository.find(new_username):
            raise UserValidationError(messages.USER_ALREADY_EXISTS)       
        return self.repository.update_username(current_username, new_username)
    
    def update_email(self, username:str, new_email:str) -> dict:
        """Actualiza el email de un usuario"""
        user = self.get_user(username)
        if user.email == new_email:
            raise SameEmailError(messages.SAME_EMAIL)
        # Validar que el nuevo email no esté registrado
        if self._email_exists(new_email):
            raise UserValidationError(messages.EMAIL_ALREADY_REGISTERED)
        user_updated = self.repository.update_email(username, new_email)
        # Mas adelante se modificara con un objeto especifico para respuestas
        return {"username": user_updated.username, "email": user_updated.email}

    def update_password(self, username: str, current_password: str, new_password: str) -> User:
        """Actualiza la contraseña de un usuario"""
        if not new_password or len(new_password) < 6:
            raise UserValidationError(messages.USER_INVALID_PASSWORD)
        user = self.get_user(username)
        # Verificar que la contraseña actual sea correcta
        if not verify_password(current_password, user.password):
            raise UserValidationError(messages.WRONG_PASSWORD)
        new_password_hash = hash_password(new_password)
        return self.repository.update_password(username, new_password_hash)
    
    def delete_user(self, username:str) -> None:
        """Elimina un usuario registrado"""
        self.repository.delete(username)

    def _email_exists(self, email: str) -> bool:
        """Verifica si un email ya está registrado"""
        existing_user = self.repository.find_by_email(email)
        return existing_user is not None
    
    def activate_user(self, username: str) -> User:
        """Activa un usuario"""
        return self.repository.update_status(username, UserStatus.ACTIVE)
    
    def deactivate_user(self, username: str) -> User:
        """Desactiva un usuario"""
        return self.repository.update_status(username, UserStatus.INACTIVE)
    
    def suspend_user(self, username: str) -> User:
        """Suspende un usuario"""
        return self.repository.update_status(username, UserStatus.SUSPENDED)
    
    def block_user(self, username: str) -> User:
        """Bloquea un usuario"""
        return self.repository.update_status(username, UserStatus.BLOCKED)
    
    def verify_user_password(self, username: str, password: str) -> bool:
        """Verifica la contraseña de un usuario"""
        user = self.get_user(username)
        return verify_password(password, user.password)