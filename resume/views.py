from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from .models import Resume
from .forms import ResumeForm
from .utils import generate_ai_summary


@login_required  # ← Only logged-in users can access this view
def resume_form_view(request):
    """
    Shows the resume form. If the user already has a resume,
    it pre-fills the form with their existing data (edit mode).
    """
    # Try to get existing resume, or None if it doesn't exist yet
    resume_instance = Resume.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume_instance)

        if form.is_valid():
            resume = form.save(commit=False)  # Don't save to DB yet
            resume.user = request.user        # Attach the logged-in user

            # Generate AI summary using Gemini
            messages.info(request, '🤖 Generating AI summary...')
            resume.summary = generate_ai_summary({
                'full_name': resume.full_name,
                'skills': resume.skills,
                'experience': resume.experience,
                'education': resume.education,
                'projects': resume.projects,
            })

            resume.save()  # Now save to database
            messages.success(request, '✅ Resume saved successfully!')
            return redirect('resume:preview')
    else:
        form = ResumeForm(instance=resume_instance)

    return render(request, 'resume/form.html', {
        'form': form,
        'is_edit': resume_instance is not None,
    })


@login_required
def resume_preview_view(request):
    """Shows the resume preview page."""
    resume = get_object_or_404(Resume, user=request.user)
    return render(request, 'resume/preview.html', {'resume': resume})


@login_required
def download_pdf_view(request):
    """
    Generates and returns a PDF of the resume.
    Uses xhtml2pdf to convert an HTML template to PDF bytes.
    """
    resume = get_object_or_404(Resume, user=request.user)

    # Load the PDF-specific template
    template = get_template('resume/pdf_template.html')
    html_string = template.render({'resume': resume})

    # Create HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation failed. Please try again.')

    return response