from django.contrib import admin
from task_manager.models import User, Task
from django.forms import CheckboxSelectMultiple


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at')
    
@admin.register(User)
class UserAdmin(ReadOnlyAdmin):
    list_display = ('id', 'name', 'email', 'mobile_no', 'created_at')
    search_fields = ('name', 'email', 'mobile_no') 
    
@admin.register(Task)
class TaskAdmin(ReadOnlyAdmin):
    list_display = ('id', 'name', 'status', 'task_type', 'completed_at')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "assigned_users":
            kwargs["widget"] = CheckboxSelectMultiple()
        return super().formfield_for_manytomany(db_field, request, **kwargs)