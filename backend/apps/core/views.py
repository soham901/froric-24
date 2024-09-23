from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CrewForm, JoinCrewForm, ExpenseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, FormView
from .models import Expense, ExpenseParticipant, Crew
from .forms import ContributionForm



def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


class CrewListView(LoginRequiredMixin, ListView):
    model = Crew
    template_name = 'core/crew_list.html'
    context_object_name = 'crews'

    def get_queryset(self):
        return self.request.user.crews.all()


class JoinCrewView(LoginRequiredMixin, FormView):
    template_name = 'core/join_crew.html'
    form_class = JoinCrewForm
    success_url = reverse_lazy('core:list_crew')


    def get_form(self):
        form = super().get_form()
        print("FORM DATA:", self.request.POST)  # Check if POST data is being received
        return form


    def form_valid(self, form):
        print("FORM IS VALID")  # Debugging message
        crew_name = form.cleaned_data.get('crew_name', None)  # Get crew_name from the form
        joining_code = form.cleaned_data.get('joining_code', None)  # Get joining_code from the form

        print(f"CREW NAME: {crew_name}")  # Log crew name
        print(f"JOINING CODE: {joining_code}")  # Log joining code

        # Validate the crew and joining code
        crew = get_object_or_404(Crew, name=crew_name, joining_code=joining_code)
        
        if self.request.user not in crew.members.all():
            crew.members.add(self.request.user)
        else:
            # User is already a member of the crew
            form.add_error(None, 'You are already a member of this crew.')

        return super().form_valid(form)


#    def form_valid(self, form):
#        print("CONTROL REACHED JOIN")
#        crew_name = form.cleaned_data['crew_name']
#        crew = get_object_or_404(Crew, name=crew_name)
#        if self.request.user not in crew.members.all():
#            crew.members.add(self.request.user)
#        return super().form_valid(form)


class CrewCreateView(LoginRequiredMixin, CreateView):
    model = Crew
    form_class = CrewForm
    template_name = 'core/create_crew.html'
    success_url = reverse_lazy('core:list_crew')

    def form_valid(self, form):
        crew = form.save()
        crew.members.add(self.request.user)
        return super().form_valid(form)


class ExpenseListView(ListView):
    model = Expense
    template_name = 'core/expense_list.html'
   
    def get_context_data(self, **kwargs):
        print(self.kwargs['crew_id'])
        print(Crew.objects.all().first().id)
        context = super().get_context_data(**kwargs)
        context['crew'] = get_object_or_404(Crew, id=self.kwargs['crew_id'])
        return context

    def get_queryset(self):
        crew_id = self.kwargs['crew_id']
        return Expense.objects.filter(crew_id=crew_id)

# OLD
class CrewExpensesView(ListView):
    model = Expense
    template_name = 'core/crew_expenses.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        crew_id = self.kwargs['crew_id']
        crew = get_object_or_404(Crew, id=crew_id)
        return Expense.objects.filter(crew=crew, is_active=True)  # Filter active expenses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crew_id = self.kwargs['crew_id']
        context['crew'] = get_object_or_404(Crew, id=crew_id)
        return context


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/expense_form.html'
    success_url = reverse_lazy('core:crew_expenses')

    def form_valid(self, form):
        print("DATA")
        form.instance.crew_id = self.kwargs['crew_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('core:crew_expenses', kwargs={'crew_id': self.kwargs['crew_id']})


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'core/expense_detail.html'
    context_object_name = 'expense'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = self.get_object()
        participants = expense.participants.all()

        # Calculate the total collected amount
        total_collected = sum(participant.amount_paid for participant in expense.participants.all())

        # Calculate the splitwise amount (total - collected)
        splitwise_amount = expense.total_amount - total_collected

        # Calculate total contributions made by each participant
        contributions = ExpenseParticipant.objects.filter(expense=expense)
        contributions_by_user = {participant.user: participant.amount_paid for participant in contributions}

        # Calculate the remaining amount for each participant
        remaining_amounts = {
            participant.user: splitwise_amount / participants.count() - contributions_by_user.get(participant.user, 0)
            for participant in participants
        }

        print(remaining_amounts)

        context['participants'] = participants
        context['splitwise'] = splitwise_amount
        context['remaining_amounts'] = remaining_amounts
        context['form'] = ContributionForm()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     expense = self.get_object()
    #     participants = expense.participants.all()

    #     # Calculate the amount each participant should contribute
    #     splitwise_amount = expense.total_amount / participants.count() if participants.count() > 0 else 0

    #     # Calculate total contributions made by each participant
    #     contributions = ExpenseParticipant.objects.filter(expense=expense)
    #     contributions_by_user = {participant.user: participant.amount_paid for participant in contributions}

    #     # Calculate the remaining amount for each participant
    #     remaining_amounts = {
    #         participant.user: splitwise_amount - contributions_by_user.get(participant.user, 0)
    #         for participant in participants
    #     }

    #     print(remaining_amounts)

    #     context['participants'] = participants
    #     context['splitwise'] = splitwise_amount
    #     context['remaining_amounts'] = remaining_amounts
    #     context['form'] = ContributionForm()
    #     return context

    def post(self, request, *args, **kwargs):
        expense = self.get_object()
        form = ContributionForm(request.POST, expense=expense)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user

            # Create or update the ExpenseParticipant entry
            participant, created = ExpenseParticipant.objects.get_or_create(
                expense=expense,
                user=user,
                defaults={'amount_paid': amount, 'amount_owed': expense.total_amount - amount}
            )
            if not created:
                participant.amount_paid += amount
                participant.amount_owed = expense.total_amount - participant.amount_paid
                participant.save()

            return redirect('core:expense_detail', pk=expense.id)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'core/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        crew_id = self.kwargs['crew_id']
        return Expense.objects.filter(crew_id=crew_id)

class ContributeToExpenseView(LoginRequiredMixin, FormView):
    form_class = ContributionForm
    template_name = 'core/contribute_to_expense.html'

    def form_valid(self, form):
        expense_id = self.kwargs['expense_id']
        expense = get_object_or_404(Expense, id=expense_id)
        user = self.request.user
        amount = form.cleaned_data.get('amount')

        participant, created = ExpenseParticipant.objects.get_or_create(
            expense=expense,
            user=user,
            defaults={'amount_paid': amount, 'amount_owed': 0}
        )

        if not created:
            participant.amount_paid += amount
            participant.save()

        return redirect('core:expense_detail', pk=expense_id)




class ContributeView(FormView):
    template_name = 'core/contribute.html'
    form_class = ContributionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        expense_id = self.kwargs['expense_id']
        expense = get_object_or_404(Expense, id=expense_id)
        kwargs['expense'] = expense
        retkwargs

    def form_valid(self, form):
        print("HERE IS THE CONTROL")
        amount = form.cleaned_data.get('amount')
        expense_id = self.kwargs['expense_id']
        expense = get_object_or_404(Expense, id=expense_id)
        user = self.request.user
        
        # Create or update the ExpenseParticipant entry
        participant, created = ExpenseParticipant.objects.get_or_create(
            expense=expense,
            user=user,
            defaults={'amount_paid': amount, 'amount_owed': expense.total_amount - amount}
        )
        if not created:
            participant.amount_paid += amount
            participant.amount_owed = expense.total_amount - participant.amount_paid
            participant.save()

        return redirect('demo:payment')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
