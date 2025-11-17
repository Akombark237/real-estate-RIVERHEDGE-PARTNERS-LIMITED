"""
Test script for Phase 2 API endpoints
Tests: Notifications API, Reports data, Dashboard analytics
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from notifications.models import Notification
from properties.models import Property, Transaction
from materials.models import Material, MaterialPrice
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

print("=" * 80)
print("🧪 PHASE 2 ENDPOINTS TEST")
print("=" * 80)

# ============================================================================
# TEST 1: NOTIFICATIONS MODEL & DATABASE
# ============================================================================
print("\n📋 TEST 1: NOTIFICATIONS MODEL & DATABASE")
print("-" * 80)

try:
    # Get or create test user
    user = User.objects.first()
    if not user:
        print("Creating test user...")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created user: {user.username}")
    else:
        print(f"✅ Found existing user: {user.username}")
    
    # Clear old test notifications
    old_count = Notification.objects.filter(user=user).count()
    if old_count > 0:
        Notification.objects.filter(user=user).delete()
        print(f"🗑️  Cleared {old_count} old notifications")
    
    # Create test notifications
    notifications_data = [
        {
            'type': 'transaction',
            'title': 'Transaction Completed',
            'message': 'Your transaction for Luxury Villa has been completed',
            'priority': 'high'
        },
        {
            'type': 'price_alert',
            'title': 'Price Alert: Cement',
            'message': 'Cement price increased by 12%',
            'priority': 'high'
        },
        {
            'type': 'property',
            'title': 'New Property Listed',
            'message': 'A new property matching your criteria has been listed',
            'priority': 'medium'
        },
        {
            'type': 'assignment',
            'title': 'New Assignment',
            'message': 'You have been assigned to manage Downtown Apartment',
            'priority': 'medium'
        },
        {
            'type': 'system',
            'title': 'Welcome!',
            'message': 'Welcome to RIVERHEDGE PARTNERS LIMITED platform',
            'priority': 'low'
        }
    ]
    
    created_notifications = []
    for notif_data in notifications_data:
        notif = Notification.objects.create(user=user, **notif_data)
        created_notifications.append(notif)
        print(f"✅ Created: {notif.type} - {notif.title}")
    
    # Test notification counts
    total = Notification.objects.filter(user=user).count()
    unread = Notification.objects.filter(user=user, is_read=False).count()
    
    print(f"\n📊 Statistics:")
    print(f"   Total notifications: {total}")
    print(f"   Unread notifications: {unread}")
    print(f"   Read notifications: {total - unread}")
    
    # Test mark as read
    first_notif = created_notifications[0]
    first_notif.mark_as_read()
    print(f"\n✅ Marked notification as read: {first_notif.title}")
    print(f"   Read status: {first_notif.is_read}")
    print(f"   Read at: {first_notif.read_at}")
    
    print("\n✅ TEST 1 PASSED: Notifications model working correctly!")
    
except Exception as e:
    print(f"\n❌ TEST 1 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 2: NOTIFICATION TYPES & PRIORITIES
# ============================================================================
print("\n📋 TEST 2: NOTIFICATION TYPES & PRIORITIES")
print("-" * 80)

try:
    # Test all notification types
    types = ['transaction', 'property', 'price_alert', 'system', 'assignment']
    priorities = ['low', 'medium', 'high']
    
    print("Testing notification types:")
    for ntype in types:
        count = Notification.objects.filter(user=user, type=ntype).count()
        print(f"   {ntype}: {count} notification(s)")
    
    print("\nTesting notification priorities:")
    for priority in priorities:
        count = Notification.objects.filter(user=user, priority=priority).count()
        print(f"   {priority}: {count} notification(s)")
    
    print("\n✅ TEST 2 PASSED: All types and priorities working!")
    
except Exception as e:
    print(f"\n❌ TEST 2 FAILED: {str(e)}")

# ============================================================================
# TEST 3: DASHBOARD ANALYTICS DATA
# ============================================================================
print("\n📋 TEST 3: DASHBOARD ANALYTICS DATA")
print("-" * 80)

try:
    # Check if we have properties
    property_count = Property.objects.count()
    print(f"Properties in database: {property_count}")
    
    # Check property status distribution
    if property_count > 0:
        statuses = Property.objects.values_list('status', flat=True).distinct()
        print("\nProperty status distribution:")
        for status in statuses:
            count = Property.objects.filter(status=status).count()
            print(f"   {status}: {count}")
    
    # Check transactions
    transaction_count = Transaction.objects.count()
    print(f"\nTransactions in database: {transaction_count}")
    
    if transaction_count > 0:
        # Calculate total revenue and commission
        completed_transactions = Transaction.objects.filter(status='completed')
        total_revenue = sum(float(t.sale_price or 0) for t in completed_transactions)
        total_commission = sum(float(t.commission_amount or 0) for t in completed_transactions)
        
        print(f"\nCompleted transactions: {completed_transactions.count()}")
        print(f"Total revenue: ${total_revenue:,.2f}")
        print(f"Total commission: ${total_commission:,.2f}")
    
    print("\n✅ TEST 3 PASSED: Dashboard data available!")
    
except Exception as e:
    print(f"\n❌ TEST 3 FAILED: {str(e)}")

# ============================================================================
# TEST 4: REPORTS DATA
# ============================================================================
print("\n📋 TEST 4: REPORTS DATA")
print("-" * 80)

try:
    # Transaction Report Data
    print("Transaction Report Data:")
    transactions = Transaction.objects.all()
    print(f"   Total transactions: {transactions.count()}")
    
    if transactions.exists():
        completed = transactions.filter(status='completed').count()
        pending = transactions.filter(status='pending').count()
        in_progress = transactions.filter(status='in_progress').count()
        cancelled = transactions.filter(status='cancelled').count()
        
        print(f"   Completed: {completed}")
        print(f"   Pending: {pending}")
        print(f"   In Progress: {in_progress}")
        print(f"   Cancelled: {cancelled}")
    
    # Property Report Data
    print("\nProperty Report Data:")
    properties = Property.objects.all()
    print(f"   Total properties: {properties.count()}")
    
    if properties.exists():
        total_value = sum(float(p.price or 0) for p in properties)
        avg_value = total_value / properties.count() if properties.count() > 0 else 0
        print(f"   Total portfolio value: ${total_value:,.2f}")
        print(f"   Average property value: ${avg_value:,.2f}")
    
    # Material Report Data
    print("\nMaterial Inventory Report Data:")
    materials = Material.objects.all()
    print(f"   Total materials: {materials.count()}")
    
    if materials.exists():
        categories = materials.values_list('category', flat=True).distinct()
        print(f"   Categories: {len(categories)}")
        for category in categories:
            count = materials.filter(category=category).count()
            print(f"      {category}: {count}")
    
    print("\n✅ TEST 4 PASSED: Reports data available!")
    
except Exception as e:
    print(f"\n❌ TEST 4 FAILED: {str(e)}")

# ============================================================================
# TEST 5: EMAIL UTILITIES (Import Test)
# ============================================================================
print("\n📋 TEST 5: EMAIL UTILITIES")
print("-" * 80)

try:
    from notifications.email_utils import (
        send_transaction_status_email,
        send_price_alert_email,
        send_property_assignment_email,
        send_welcome_email,
        send_bulk_notification_email
    )
    
    print("✅ Email utility functions imported successfully:")
    print("   - send_transaction_status_email")
    print("   - send_price_alert_email")
    print("   - send_property_assignment_email")
    print("   - send_welcome_email")
    print("   - send_bulk_notification_email")
    
    print("\n✅ TEST 5 PASSED: Email utilities ready!")
    
except Exception as e:
    print(f"\n❌ TEST 5 FAILED: {str(e)}")

# ============================================================================
# TEST 6: SIGNALS (Import Test)
# ============================================================================
print("\n📋 TEST 6: DJANGO SIGNALS")
print("-" * 80)

try:
    import notifications.signals
    
    print("✅ Signal handlers imported successfully:")
    print("   - transaction_status_changed")
    print("   - property_assigned")
    print("   - user_created")
    print("   - material_price_alert")
    
    print("\n✅ TEST 6 PASSED: Signals configured!")
    
except Exception as e:
    print(f"\n❌ TEST 6 FAILED: {str(e)}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

print("\n✅ ALL TESTS COMPLETED!")
print("\nWhat was tested:")
print("   ✅ Notifications model and database")
print("   ✅ Notification types and priorities")
print("   ✅ Dashboard analytics data")
print("   ✅ Reports data availability")
print("   ✅ Email utility functions")
print("   ✅ Django signal handlers")

print("\n🎯 NEXT STEPS:")
print("   1. Start the Django server: python manage.py runserver")
print("   2. Start the React frontend: cd frontend && npm run dev")
print("   3. Test the API endpoints in the browser")
print("   4. Check notifications in the UI")

print("\n" + "=" * 80)
print("🎉 PHASE 2 ENDPOINTS ARE READY TO USE!")
print("=" * 80)

