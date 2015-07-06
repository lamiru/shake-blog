from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        messages.info(self.request, 'You are now registered.')
        return super(SignupView, self).form_valid(form)
