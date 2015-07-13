from django.contrib import messages


class FormValidMessageMixin(object):
    form_valid_message = None

    def form_valid(self, form):
        if self.form_valid_message is not None:
            messages.info(self.request, self.form_valid_message)
        return super(FormValidMessageMixin, self).form_valid(form)

    def delete(self, request, *args, **kwargs):
        if self.form_valid_message is not None:
            messages.error(request, self.form_valid_message)
        return super(FormValidMessageMixin, self).delete(request, *args, **kwargs)  # noqa
