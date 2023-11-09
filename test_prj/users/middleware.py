from .models import User
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseForbidden

from datetime import timedelta


def get_client_ip(request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr
    
class IP_Middleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        if '/users/' in str(request.path) and "admin" not in str(request.path):
            client_ip = get_client_ip(request)
            
            try:
                # Fetching Data of User from IP
                user = User.objects.get(ip = client_ip)
                current_time = timezone.now()
                
                if user.status == "blocked":
                    if user.unblock_time is not None: # Because unblock_time can be None
                        if user.unblock_time < current_time:
                            user.status = "unblock"
                            user.req_count = 0 
                            user.unblock_time = None
                            user.save()
                        else:
                            return HttpResponseForbidden("<h1>BLOCKED !!!!!</h1>")
                else:
                    if user.req_count >= 5:
                        user.status = "blocked"
                        user.unblock_time = timezone.now() + timedelta(minutes = 10)       
                        user.req_count += 1
                        user.save()
                    else:
                        user.req_count += 1
                        user.save()     
            except User.DoesNotExist:
                
                # Creating User if not Found (First Time User)
                user = User.objects.create(name = f"user_{client_ip}",
                                    ip = client_ip)
        
        response = self.get_response(request)
        return response
    
    
    
    
    
