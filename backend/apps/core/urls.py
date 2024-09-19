from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Crew
    path('crew/create/', views.CrewCreateView.as_view(), name='create_crew'),
    path('crew/join/', views.JoinCrewView.as_view(), name='join_crew'),
    path('crew/', views.CrewListView.as_view(), name='list_crew'),

    # Expense
    path('<int:crew_id>/expenses/', views.ExpenseListView.as_view(), name='crew_expenses'),
    path('<int:crew_id>/expenses/new/', views.ExpenseCreateView.as_view(), name='create_expense'),

    path('expense/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense/<int:expense_id>/contribute/', views.ContributeToExpenseView.as_view(), name='contribute_to_expense'),


    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
