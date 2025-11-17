"""
Django signals for automatic email notifications
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .email_utils import (
    send_transaction_status_email,
    send_property_assignment_email,
    send_welcome_email
)
from .models import Notification

User = get_user_model()


@receiver(post_save, sender='properties.Transaction')
def transaction_status_changed(sender, instance, created, **kwargs):
    """
    Send email notification when transaction status changes
    """
    if not created:  # Only for updates, not new transactions
        # Check if status changed
        if instance.pk:
            try:
                old_instance = sender.objects.get(pk=instance.pk)
                if old_instance.status != instance.status:
                    # Send email to buyer, seller, and agent
                    users_to_notify = []
                    
                    if instance.buyer:
                        users_to_notify.append(instance.buyer)
                    if instance.seller:
                        users_to_notify.append(instance.seller)
                    if instance.agent:
                        users_to_notify.append(instance.agent)
                    
                    for user in users_to_notify:
                        if user and user.email:
                            send_transaction_status_email(instance, user)
                            
                            # Also create in-app notification
                            Notification.objects.create(
                                user=user,
                                type='transaction',
                                title=f'Transaction Status Updated: {instance.property.title}',
                                message=f'Transaction status changed to {instance.get_status_display()}',
                                priority='high' if instance.status == 'completed' else 'medium',
                                related_id=instance.id,
                                related_type='transaction'
                            )
            except sender.DoesNotExist:
                pass


@receiver(post_save, sender='properties.Property')
def property_assigned(sender, instance, created, **kwargs):
    """
    Send email notification when property is assigned to an agent
    """
    if not created and instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Check if agent changed
            if old_instance.agent != instance.agent and instance.agent:
                send_property_assignment_email(instance, instance.agent)
                
                # Create in-app notification
                Notification.objects.create(
                    user=instance.agent,
                    type='assignment',
                    title=f'New Property Assignment: {instance.title}',
                    message=f'You have been assigned to manage {instance.title} in {instance.city}',
                    priority='medium',
                    related_id=instance.id,
                    related_type='property'
                )
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    Send welcome email to new users
    """
    if created and instance.email:
        send_welcome_email(instance)
        
        # Create welcome notification
        Notification.objects.create(
            user=instance,
            type='system',
            title='Welcome to RIVERHEDGE PARTNERS LIMITED!',
            message='Your account has been created successfully. Explore the platform and start managing your real estate business.',
            priority='low'
        )


@receiver(post_save, sender='materials.MaterialPrice')
def material_price_alert(sender, instance, created, **kwargs):
    """
    Send price alert when material price changes significantly
    """
    if created and instance.material:
        # Get previous price
        previous_prices = sender.objects.filter(
            material=instance.material
        ).exclude(id=instance.id).order_by('-recorded_at')[:1]
        
        if previous_prices.exists():
            previous_price = previous_prices.first()
            price_change_percent = abs(
                (float(instance.price) - float(previous_price.price)) / float(previous_price.price) * 100
            )
            
            # Alert if price changed by more than 10%
            if price_change_percent > 10:
                # Get all admin users and agents
                users_to_notify = User.objects.filter(
                    role__in=['admin', 'agent']
                )
                
                for user in users_to_notify:
                    if user.email:
                        from .email_utils import send_price_alert_email
                        send_price_alert_email(
                            instance.material,
                            instance,
                            user,
                            previous_price.price
                        )
                        
                        # Create in-app notification
                        Notification.objects.create(
                            user=user,
                            type='price_alert',
                            title=f'Price Alert: {instance.material.name}',
                            message=f'Price changed by {price_change_percent:.1f}% - Now ${instance.price}',
                            priority='high',
                            related_id=instance.material.id,
                            related_type='material'
                        )

