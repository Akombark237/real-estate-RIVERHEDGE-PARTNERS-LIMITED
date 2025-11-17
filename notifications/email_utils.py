"""
Email notification utilities for sending automated emails
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_transaction_status_email(transaction, user):
    """
    Send email notification when transaction status changes
    
    Args:
        transaction: Transaction object
        user: User to notify
    """
    subject = f'Transaction Status Update: {transaction.property.title}'
    
    context = {
        'user': user,
        'transaction': transaction,
        'property': transaction.property,
        'status': transaction.get_status_display(),
    }
    
    # Render HTML email
    html_message = render_to_string('emails/transaction_status.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send transaction status email: {e}")
        return False


def send_price_alert_email(material, price, user, threshold):
    """
    Send email notification when material price exceeds threshold
    
    Args:
        material: Material object
        price: MaterialPrice object
        user: User to notify
        threshold: Price threshold that was exceeded
    """
    subject = f'Price Alert: {material.name} - Price Change Detected'
    
    context = {
        'user': user,
        'material': material,
        'price': price,
        'threshold': threshold,
        'change_percent': ((float(price.price) - float(threshold)) / float(threshold) * 100),
    }
    
    html_message = render_to_string('emails/price_alert.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send price alert email: {e}")
        return False


def send_property_assignment_email(property_obj, agent):
    """
    Send email notification when property is assigned to an agent
    
    Args:
        property_obj: Property object
        agent: User (agent) who was assigned
    """
    subject = f'New Property Assignment: {property_obj.title}'
    
    context = {
        'agent': agent,
        'property': property_obj,
    }
    
    html_message = render_to_string('emails/property_assignment.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[agent.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send property assignment email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to new users
    
    Args:
        user: User object
    """
    subject = 'Welcome to RIVERHEDGE PARTNERS LIMITED Real Estate Platform'
    
    context = {
        'user': user,
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        return False


def send_bulk_notification_email(users, subject, message, html_message=None):
    """
    Send bulk email notification to multiple users
    
    Args:
        users: List of User objects
        subject: Email subject
        message: Plain text message
        html_message: Optional HTML message
    """
    recipient_list = [user.email for user in users if user.email]
    
    if not recipient_list:
        return False
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send bulk email: {e}")
        return False

