from django.contrib import admin
from .models import Crew, Expense, Payment, Balance, ExpenseParticipant
from .resources import ExpenseResource
from import_export.admin import ExportActionModelAdmin

admin.site.site_header = "FatafatSettle"
admin.site.site_title = "FatafatSettle"
admin.site.index_title = "FatafatSettle"


admin.site.register(Crew)
admin.site.register(Payment)
admin.site.register(Balance)
admin.site.register(ExpenseParticipant)


class ExpenseAdmin(ExportActionModelAdmin):
    resource_class = ExpenseResource
    list_display = ('id', 'name', 'total_amount', 'date')
    search_fields = ('name',)

admin.site.register(Expense, ExpenseAdmin)

