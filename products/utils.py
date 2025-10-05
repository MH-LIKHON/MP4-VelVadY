# =======================================================
# CORE UTILS: Base URL resolver
# =======================================================

from django.conf import settings

def get_base_url(request=None) -> str:
    """
    Returns the base URL to build absolute links (emails, Stripe callbacks).
    Priority:
      1) Explicit settings.DOMAIN (best: set via environment)
      2) request.build_absolute_uri("/") when a request is available
      3) Safe dev fallback to http://127.0.0.1:8000
    """
    # 1) Explicit environment-driven domain (preferred for dev/VM/prod)
    domain = getattr(settings, "DOMAIN", None)
    if domain:
        return domain.rstrip("/")

    # 2) Derive from the current request (keeps scheme/host/port)
    if request is not None:
        return request.build_absolute_uri("/").rstrip("/")

    # 3) Dev fallback
    return "http://127.0.0.1:8000"