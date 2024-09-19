from import_export import resources
from .models import Expense

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense
        fields = ('id', 'name', 'total_amount', 'date')
