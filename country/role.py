from django.shortcuts import redirect

class AccessRole:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            # if request.user.is_staff:
            allow_urls =[
                "/admin/",
                "/list-user/",
                "/list-product/",
            ]
            for url in allow_urls:
                if request.path.startswith(url):
                    return self.get_response(request)
            return redirect("/admin/")
        return self.get_response(request)