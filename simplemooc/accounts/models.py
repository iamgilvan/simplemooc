import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Create your models here.
# Em settings deverá ser adicionado o AUTH_USER_MODEL para indicar este novo model
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True, 
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email       = models.EmailField('E-mail', unique=True)
    name        = models.CharField('Nome', max_length=100, blank=True)

    # Manter compatibilidade com o Admin
    # Ver https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms
    is_active   = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff    = models.BooleanField('É da equipe?', blank=True, default=False)

    # 'auto_now_add' tells Django that when you add a new row, you want the current date & time added. 
    # 'auto_now' tells Django to add the current date & time will be added EVERY time the record is saved.    
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD  = 'username'# campo que vai ser a referencia no login e tb é unico
    REQUIRED_FIELDS = ['email'] # Utilizado na criação de superusuário.

    def __str__(self): # representação de string do usuário
        return self.name or self.username # se nao tiver o name retorna o username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name        = 'Usuário'
        verbose_name_plural = 'Usuários'

# Após isso vamos apagar o banco e as pastas migrations de accounts e courses.
#>mv db.sqlite3 db.sqlite3.old
#recriá-lo com o novo model
#>python manage.py makemigrations accounts
#>python manage.py makemigrations courses
#>python manage.py migrate 
#>python manage.py showmigrations
#criar um superuser
#>python manage.py createsuperuser
#>sqlite3 db.sqlite3 
#sqlite> PRAGMA table_info(accounts_user); # ver as colunas da nova tabela