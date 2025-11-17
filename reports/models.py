from django.db import models


class Report(models.Model):
    """Generated reports model"""

    REPORT_TYPE_CHOICES = [
        ('price_trends', 'Price Trends'),
        ('sales_performance', 'Sales Performance'),
        ('market_analysis', 'Market Analysis'),
        ('commission', 'Commission Report'),
        ('inventory', 'Inventory Report'),
        ('custom', 'Custom Report'),
    ]

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')

    # Report parameters (stored as JSON)
    parameters = models.JSONField(default=dict)

    # Generated file
    file = models.FileField(upload_to='reports/', null=True, blank=True)

    # User who generated the report
    generated_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reports')

    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} - {self.generated_at.date()}"
