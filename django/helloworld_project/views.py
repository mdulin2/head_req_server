from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')

@method_decorator(csrf_exempt, name='dispatch')
class firstView(View):
    @csrf_exempt
    def post(self, request):
        print ("POST....")
        return HttpResponse('Post!') 
    def get(self, request):
        print ("GET...." )
        return HttpResponse('GET!') 
    @csrf_exempt
    def put(self, request):
        print("put....")
        return HttpResponse('put!') 
    @csrf_exempt
    def patch(self, request):
        print ("patch...." )
        return HttpResponse('patch!') 
    
    def delete(self, request):
        print ("delete....")
        return HttpResponse('delete!') 
    '''
    def head(self, request):
        print ("HEAD...." )
        return HttpResponse('HEAD!')  
    '''
    def options(self, request):
        print("options....")
        return HttpResponse('options!') 
    
    def trace(self, request):
        print("trace....")
        return HttpResponse('trace!') 
    
    # Does not work, even if we try to define it. 
    def connect(self, request):
        print("connect....")
        return HttpResponse('Connect!') 

''' 
This example shows that this request works (and gets hit) for a head request 
This example does not work with a head request if the http_methods are set to just GET and POST
The method decorator is quite strict on this. 
'''
#@require_http_methods(["GET", "POST"])
@method_decorator(csrf_exempt, name='dispatch')
def index(request): 
    if(request.method == 'GET'):
        print("do GET stuff")
    else: 
        print("Do other stuff")
    return HttpResponse(str(request.method))