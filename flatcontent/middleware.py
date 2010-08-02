class NewUserMiddleware(object):
    """
    Determines wither the request is from a new user. MUST come AFTER the 
    session middleware in the stack to work properly. 
    """
    def process_request(self, request):
        if 'new_user' not in request.session:
            request.session['new_user'] = True

    def process_response(self, request, response):
        request.session['new_user'] = False
        return response
