from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Crew(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    joining_code = models.CharField(max_length=100, default='')
    members = models.ManyToManyField(User, related_name='crews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='general')
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.description} - {self.total_amount}"

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_participations')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} - Paid: {self.amount_paid}, Owed: {self.amount_owed}"

class Payment(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='payments')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer} paid {self.amount} to {self.recipient}"

class Balance(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='balances')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_balance')
        ]

    def __str__(self):
        return f"{self.user}'s balance in {self.crew}: {self.amount}"

