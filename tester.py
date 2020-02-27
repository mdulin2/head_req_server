import requests as r 
import subprocess

# Sends each HTTP request type to a given URL 
# This even includes an invalid HTTP header
def request_sender(url):
    get_result = r.get(url).text 
    print("GET result...", get_result)

    post_result = r.post(url).text
    print("POST result...", post_result)

    put_result = r.put(url).text
    print("PUT result...", put_result)

    patch_result = r.patch(url).text 
    print("PATCH result...", patch_result)

    head_result = r.head(url).text 
    print("HEAD result...", head_result)

    option_result = r.delete(url).text
    print("DELETE result...", option_result)

    option_result = r.options(url).text
    print("OPTION result...", option_result)

    # Typically, this method is not allowed unless specified
    trace_result = subprocess.run(["curl", "-v", "-X", "TRACE", url],stdout=subprocess.PIPE)
    print(trace_result)

    # Typically, this method is not even used.
    connect_result = subprocess.run(["curl", "-v", "-X", "CONNECT", url],stdout=subprocess.PIPE)
    print(connect_result)

    # This should give some sort of error.
    invalid_result = subprocess.run(["curl", "-v", "-X", "??", url],stdout=subprocess.PIPE)
    print(invalid_result)

# request_sender("http://127.0.0.1:8000/") # For Django 
# request_sender("http://127.0.0.1:5000/login-unsafe") # For Flask 
#request_sender("http://127.0.0.1:3000") # For nodejs
#request_sender("http://127.0.0.1:9000") # For Spring
