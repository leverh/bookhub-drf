class CSRFTrustedOriginsMiddleware:
    """
    Middleware to handle CSRF for cross-origin requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __process_request(self, request):
        # Get the Origin or Referer header
        referer = request.META.get('HTTP_REFERER', '')
        origin = request.META.get('HTTP_ORIGIN', '')
        
        # List of trusted origins
        trusted_origins = [
            'https://bookhub-lime.vercel.app',
            'http://localhost:3000',
            'https://bookhub-gae6.onrender.com',
        ]
        
        # Check if the origin is trusted
        is_trusted = False
        for trusted in trusted_origins:
            if referer.startswith(trusted) or origin.startswith(trusted):
                is_trusted = True
                break
        
        # If trusted origin, skip CSRF checks for non-GET requests
        if is_trusted and request.method != 'GET':
            request._dont_enforce_csrf_checks = True

    def __call__(self, request):
        self.__process_request(request)
        response = self.get_response(request)
        return response