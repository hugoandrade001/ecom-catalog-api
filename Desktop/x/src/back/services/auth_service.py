from back.model.user import User
from back import db

class AuthService:
   
    @staticmethod
    def authenticate(username, password):
        """
        Autentica um usu�rio verificando username e password

        Args:
            username (str): Username do usu�rio
            password (str): Senha em texto plano

        Returns:
            User: Objeto do usu�rio se autenticado, None caso contr�rio
        """
        # Busca usu�rio por username
        user = User.query.filter_by(username=username).first()

        # Verifica se existe e se a senha est� correta
        if user and user.check_password(password):
            return user

        return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Busca um usu�rio por ID

        Args:
            user_id (int): ID do usu�rio

        Returns:
            User: Objeto do usu�rio ou None
        """
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, email, password):
        """
        Cria um novo usu�rio no banco

        Args:
            username (str): Username �nico
            email (str): Email �nico
            password (str): Senha em texto plano 

        Returns:
            User: Usu�rio criado ou None se houver erro
        """
        try:
            # Verifica se j� existe
            if User.query.filter_by(username=username).first():
                raise ValueError('Username já existe')

            if User.query.filter_by(email=email).first():
                raise ValueError('Email já existe')

            # Cria novo usu�rio
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return user

        except Exception as e:
            db.session.rollback()
            raise e
