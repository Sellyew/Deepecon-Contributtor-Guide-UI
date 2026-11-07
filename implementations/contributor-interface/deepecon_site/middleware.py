"""Security headers for every response (plan §3: no external assets)."""

CONTRIBUTOR_CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; "
    "connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
)
# Django's administration pages use some inline style attributes; they are for the team only
# and still load nothing from other sites.
ADMIN_CSP = CONTRIBUTOR_CSP.replace("style-src 'self'", "style-src 'self' 'unsafe-inline'")


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = ADMIN_CSP if request.path.startswith("/team-admin/") else CONTRIBUTOR_CSP
        response.headers.setdefault("Content-Security-Policy", csp)
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=(), interest-cohort=()")
        response.headers.setdefault("Cache-Control", "no-store")
        if request.path.startswith("/i/"):
            response.headers["Referrer-Policy"] = "no-referrer"     # invitation tokens never leave in a Referer
        return response
