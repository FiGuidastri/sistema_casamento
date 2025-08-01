# casamento/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Casal, Fornecedor, Cerimonialista

@receiver(post_save, sender=Usuario)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Cria um perfil correspondente (Casal, Fornecedor, etc.)
    automaticamente sempre que um novo Usuario é criado.
    """
    if created: # Apenas executa se o usuário foi recém-criado
        if instance.tipo_usuario == 'CASAL':
            Casal.objects.create(usuario=instance)
        elif instance.tipo_usuario == 'FORNECEDOR':
            Fornecedor.objects.create(usuario=instance)
        elif instance.tipo_usuario == 'CERIMONIALISTA':
            Cerimonialista.objects.create(usuario=instance)