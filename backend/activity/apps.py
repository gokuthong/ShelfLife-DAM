from django.apps import AppConfig

<<<<<<< HEAD

class ActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity'
=======
class ActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity'
    verbose_name = 'Activity & Collaboration'
>>>>>>> 3068d61 (advanced filters, comments CRUD, and role-based permissions)
