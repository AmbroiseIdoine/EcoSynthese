from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import get_template

from .models import Sujet, Secteur, Picture, Page
from .forms import ContactForm


def page_view(request, page_name):
    page = get_object_or_404(Page, name=page_name)
    return render(request, 'ecosyn/page.html', {"object":page})

def home(request):
    page = get_object_or_404(Page, name="Accueil")
    secteur_list = Secteur.objects.order_by('-name').all()
    context={"object":page, "secteur_list":secteur_list}
    return render(request,'ecosyn/home.html',context)

def apropos(request):
    return page_view(request, "A propos")
    
def sources(request):
    return page_view(request, "Sources")
    
def contact(request):
    form_class = ContactForm
    context = {"form": form_class}
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            contact_subject = request.POST.get('contact_subject', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_subject': contact_subject,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "EcoSynthese" +'',
                ['ambroise94@live.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')
            
    return render(request, 'ecosyn/contact.html', context)
    
class ContactView(generic.base.TemplateView):
    template_name = 'ecosyn/contact.html'
        
class ReportView(generic.ListView):
    template_name = 'ecosyn/reports.html'
    
    def get_queryset(self):
        """ Return the last ten published reports """
        return Secteur.objects.order_by('-name')
        
class TopicView(generic.ListView):
    template_name = 'ecosyn/topics.html'
    def get_queryset(self):
        """ Return all existing topics """
        return Sujet.objects.order_by('-name')

class ReportDetailView(generic.DetailView):
    model = Secteur
    template_name = 'ecosyn/report_details.html'
    
class TopicDetailView(generic.DetailView):
    model = Sujet 
    template_name = 'ecosyn/topic_details.html'



















