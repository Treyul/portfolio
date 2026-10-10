import json
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def app_shell(request, *args, **kwargs):
    """Serve the React app for every client-side route."""
    return render(request, 'index.html')


@csrf_exempt
def api_contact(request):
    """Validate a contact submission and deliver it to the configured inbox."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    try:
        data = json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)

    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    subject = str(data.get('subject', '')).strip()
    message = str(data.get('message', '')).strip()
    if not all((name, email, subject, message)):
        return JsonResponse({'error': 'All fields are required.'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

    recipient = getattr(settings, 'CONTACT_EMAIL', '')
    if not recipient:
        return JsonResponse({'error': 'Contact email is not configured.'}, status=503)

    body = f'From: {name} <{email}>\n\n{strip_tags(message)}'
    try:
        EmailMessage(
            subject=f'Portfolio contact: {subject}',
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[email],
        ).send(fail_silently=False)
    except Exception:
        logger.exception('Contact email delivery failed')
        return JsonResponse({'error': 'Unable to send your message right now.'}, status=502)

    return JsonResponse({
        'success': True,
        'message': 'Thank you for your message! I will get back to you soon.',
    })
