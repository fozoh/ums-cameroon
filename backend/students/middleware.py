# backend/students/middleware.py
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect
from .models import License, Institution
from django.conf import settings
from django.utils import timezone
import re

class LicenseMiddleware:
    """
    Ensures the system operates only under a valid license.
    Blocks access if:
    - No license exists
    - License is expired
    - Domain is not authorized
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip license check for admin login and static/media files
        if (
            request.path.startswith('/admin/') or
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/api/login') or
            request.path == '/api/health/' or
            request.path == '/license/setup/' or
            request.path == '/license/activate/' or
            request.path.startswith('/api/license')
        ):
            return self.get_response(request)

        try:
            license = License.objects.latest('valid_until')
            if not self.is_active(license):
                return HttpResponseForbidden("License expired. Please renew.")
            if not self.is_domain_allowed(license, request):
                return HttpResponseForbidden("This domain is not licensed.")
        except License.DoesNotExist:
            return HttpResponseForbidden("No valid license found. Please contact support.")

        return self.get_response(request)

    def is_active(self, license):
        """Check if license is within validity period"""
        from datetime import date
        today = date.today()
        return license.valid_from <= today <= license.valid_until

    def is_domain_allowed(self, license, request):
        """Check if current domain is in allowed domains"""
        allowed_domains = license.domains.strip().splitlines()
        allowed_domains = [d.strip() for d in allowed_domains if d.strip()]
        
        current_host = request.get_host().split(':')[0]  # Remove port
        
        # Support wildcard subdomains (e.g., *.univyaounde.cm)
        for domain in allowed_domains:
            if domain.startswith('*.'):
                pattern = r'^.+\.%s$' % re.escape(domain[2:])
                if re.match(pattern, current_host):
                    return True
            elif domain == current_host:
                return True
        return False


class TenantMiddleware:
    """
    Enables multi-tenancy: one UMS server serving multiple institutions
    Each institution has isolated data based on domain
    e.g., ums.univyaounde.cm → University of Yaoundé
          ums.univbuea.cm → University of Buea
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for static/media and setup
        if (
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/admin/') or
            request.path == '/setup/' or
            request.path == '/api/health/'
        ):
            return self.get_response(request)

        host = request.get_host().split(':')[0]  # Remove port

        # Allow localhost and 127.0.0.1 for development
        if host in ['localhost', '127.0.0.1'] and settings.DEBUG:
            try:
                request.tenant = Institution.objects.first() or Institution.objects.create(
                    name="Development Institution",
                    domain="localhost",
                    license_key="DEV-LOCALHOST",
                    valid_until="2030-12-31",
                    is_active=True
                )
            except:
                pass  # DB not ready yet
            return self.get_response(request)

        try:
            tenant = Institution.objects.get(domain=host)
            if not tenant.is_active:
                return HttpResponseForbidden("Institution suspended.")
            if tenant.valid_until < timezone.now().date():
                return HttpResponseForbidden("Institution license expired.")
            
            request.tenant = tenant
        except Institution.DoesNotExist:
            return HttpResponseForbidden(
                f"No institution configured for domain: {host}<br><br>"
                "Please contact your IT department or UMS support.<br><br>"
                "<a href='https://ums-cmr.cm'>ums-cmr.cm</a>", 
                content_type="text/html"
            )
        except Exception as e:
            return HttpResponseForbidden(f"System error: {str(e)}")

        return self.get_response(request)


# Optional: Admin Only Middleware
class AdminAccessMiddleware:
    """
    Restrict certain paths to admin users only
    Use: 'MIDDLEWARE': [..., 'students.middleware.AdminAccessMiddleware']
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [
            '/admin-portal/',
            '/reports/',
            '/sms/send/',
            '/license/renew/',
            '/students/import/'
        ]
        
        if any(request.path.startswith(path) for path in restricted_paths):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('student-login')}?next={request.path}")
            if not request.user.role in ['admin', 'finance', 'registrar', 'hod', 'dean']:
                return HttpResponseForbidden("Access denied.")
        
        return self.get_response(request)