from django.views.generic.base import TemplateView

# Create your views here.

class MentionsLegalesView(TemplateView):
    template_name = 'legal/mentions_legales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AlignedOrgsView(TemplateView):
    template_name = 'legal/aligned_orgs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SponsorView(TemplateView):
    template_name = 'legal/sponsor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class VolunteerView(TemplateView):
    template_name = 'legal/volunteer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
