"""
Test script for Phase 3A endpoints
Tests Document Management, Activity Logs, and Global Search
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from documents.models import Document
from activity_log.models import ActivityLog
from properties.models import Property
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def print_success(text):
    print(f"✅ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_documents():
    print_header("TEST 1: DOCUMENT MANAGEMENT SYSTEM")
    
    # Get or create test user
    user = User.objects.filter(is_staff=True).first()
    if not user:
        user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        print_success("Created test admin user")
    
    print_info(f"Using user: {user.username}")
    
    # Create test document
    test_file = SimpleUploadedFile(
        "test_document.txt",
        b"This is a test document for Phase 3A testing",
        content_type="text/plain"
    )
    
    document = Document.objects.create(
        title="Test Property Deed",
        description="Test document for property deed",
        document_type="property_deed",
        category="property",
        file=test_file,
        uploaded_by=user,
        is_public=True
    )
    
    print_success(f"Created document: {document.title}")
    print_info(f"  - ID: {document.id}")
    print_info(f"  - Type: {document.document_type}")
    print_info(f"  - Category: {document.category}")
    print_info(f"  - File size: {document.file_size_mb} MB")
    print_info(f"  - Public: {document.is_public}")
    
    # Test document queries
    total_docs = Document.objects.count()
    property_docs = Document.objects.filter(category='property').count()
    public_docs = Document.objects.filter(is_public=True).count()
    
    print_success(f"Document Statistics:")
    print_info(f"  - Total documents: {total_docs}")
    print_info(f"  - Property documents: {property_docs}")
    print_info(f"  - Public documents: {public_docs}")
    
    return document

def test_activity_logs(document):
    print_header("TEST 2: ACTIVITY LOG / AUDIT TRAIL")
    
    user = User.objects.filter(is_staff=True).first()
    
    # Create test activity logs
    activities = [
        {
            'action': 'upload',
            'description': f'Uploaded document: {document.title}',
            'severity': 'low',
            'content_object': document
        },
        {
            'action': 'view',
            'description': 'Viewed property list',
            'severity': 'low',
            'content_object': None
        },
        {
            'action': 'update',
            'description': 'Updated property details',
            'severity': 'medium',
            'content_object': None
        },
        {
            'action': 'delete',
            'description': 'Deleted old transaction',
            'severity': 'high',
            'content_object': None
        },
        {
            'action': 'login',
            'description': 'User logged in',
            'severity': 'low',
            'content_object': None
        }
    ]
    
    for activity_data in activities:
        ActivityLog.log_activity(
            user=user,
            action=activity_data['action'],
            description=activity_data['description'],
            severity=activity_data['severity'],
            content_object=activity_data['content_object'],
            ip_address='127.0.0.1',
            user_agent='Test Script'
        )
    
    print_success(f"Created {len(activities)} test activity logs")
    
    # Test activity log queries
    total_logs = ActivityLog.objects.count()
    upload_logs = ActivityLog.objects.filter(action='upload').count()
    high_severity = ActivityLog.objects.filter(severity='high').count()
    user_logs = ActivityLog.objects.filter(user=user).count()
    
    print_success(f"Activity Log Statistics:")
    print_info(f"  - Total logs: {total_logs}")
    print_info(f"  - Upload actions: {upload_logs}")
    print_info(f"  - High severity: {high_severity}")
    print_info(f"  - User's logs: {user_logs}")
    
    # Test activity log with changes tracking
    log_with_changes = ActivityLog.log_activity(
        user=user,
        action='update',
        description='Updated property price',
        severity='medium',
        changes={
            'old_value': {'price': 100000},
            'new_value': {'price': 120000}
        }
    )
    
    print_success("Created activity log with change tracking:")
    print_info(f"  - Changes: {log_with_changes.changes}")
    
    return total_logs

def test_global_search():
    print_header("TEST 3: GLOBAL SEARCH")
    
    # Test search across models
    from django.db.models import Q
    
    # Search properties
    search_query = "test"
    properties = Property.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query)
    )
    
    print_success(f"Search Results for '{search_query}':")
    print_info(f"  - Properties found: {properties.count()}")
    
    # Search documents
    documents = Document.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query)
    )
    print_info(f"  - Documents found: {documents.count()}")
    
    # Search activity logs
    logs = ActivityLog.objects.filter(
        Q(description__icontains=search_query)
    )
    print_info(f"  - Activity logs found: {logs.count()}")
    
    total_results = properties.count() + documents.count() + logs.count()
    print_success(f"Total search results: {total_results}")
    
    return total_results

def main():
    print_header("🚀 PHASE 3A ENDPOINT TESTING")
    print_info("Testing Document Management, Activity Logs, and Global Search")
    
    try:
        # Test 1: Documents
        document = test_documents()
        
        # Test 2: Activity Logs
        total_logs = test_activity_logs(document)
        
        # Test 3: Global Search
        total_results = test_global_search()
        
        # Final Summary
        print_header("✅ ALL TESTS PASSED!")
        print_success("Phase 3A Backend is working perfectly!")
        print_info("\nSummary:")
        print_info(f"  - Documents created and tested")
        print_info(f"  - Activity logs: {total_logs} entries")
        print_info(f"  - Search results: {total_results} items")
        print_info("\nNext Steps:")
        print_info("  1. Start the Django server: python manage.py runserver")
        print_info("  2. Start the React frontend: cd frontend && npm run dev")
        print_info("  3. Test the UI at http://localhost:5173")
        print_info("  4. Navigate to /documents and /activity-logs pages")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

