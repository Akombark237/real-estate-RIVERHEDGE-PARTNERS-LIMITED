from django.contrib import admin
from .models import CostEstimate, EstimateItem, ProjectTemplate


class EstimateItemInline(admin.TabularInline):
    model = EstimateItem
    extra = 1


@admin.register(CostEstimate)
class CostEstimateAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'project_type', 'user', 'total_cost', 'status', 'estimate_date']
    list_filter = ['project_type', 'quality_level', 'status', 'estimate_date']
    search_fields = ['project_name', 'user__email', 'description']
    inlines = [EstimateItemInline]
    date_hierarchy = 'estimate_date'


@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_type', 'quality_level', 'is_active', 'created_at']
    list_filter = ['project_type', 'quality_level', 'is_active']
    search_fields = ['name', 'description']
