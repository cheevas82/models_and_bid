from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Role(models.TextChoices):
	M1 = 'M1', 'МЕНЕДЖЕР1'
	M2 = 'M2', 'МНЕДЖЕР2'
	Logic = 'Logic', 'логист'
	M3 = 'M3', 'менеджер направления'
	BOSS = 'BOSS', 'казначей'
	Buh = 'Buh', 'БУХ'



class User(AbstractUser):
	role = models.CharField(max_length=15, choices=Role.choices, default=Role.M2)
	email = models.EmailField(
		_("email address"),
		unique=True,
		)
	email_verify = models.BooleanField(default=False)

	REQUIRED_FIELDS = ["username"]
	USERNAME_FIELD = "email"
    
