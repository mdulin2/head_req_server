# Request Handling Based Upon Methods

## Introduction 

Some security issues are quite obvious and easy to find based upon very simple patterns. However, there are others that lie deep below the surface, stemming from the developer not understanding the technology they were using and implementing unsound logic. These types of bugs tend to be very subtle. 
  
Today, I wanted to share another item to add to the tool belt. This bug comes from two main insights: developers can programmatically route requests based upon their request method and most backend servers automatically map *HEAD* requests to *GET* requests. The next few sections will dive into *why* this is the case and *how* these features can be used bypass security mechanisms. Finally, we will see which backend web frameworks are potentially vulnerable to this type of attack. 

## Request Types 

The HTTP protocol has a set of **request** methods that allow/describe the action to be performed on a resource. These *methods* are commonly referred to as HTTP verbs. All of these verbs have they own specific purpose. For this post, there are three main verb categories we will talk about: 
- GET 
- HEAD 
- State Changing Verbs (POST, PUT, DELETE, PATCH) 

The *GET* verb is the most common request, which just *gets* data for the user. A *HEAD* request is exactly the same as a *GET* request except that no data is returned to the user; only the headers are returned from the request. Finally, several requests are only for altering data (POST,PUT, DELETE and PATCH). For the purpose of this article, no other information is needed, as it is irrelevant for the findings. If you would like to learn more about the different request methods, please visit https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods. 

## Request Mappings 

When creating API's, the proper functionality is chosen based upon the *URL*, parameters and the *request method*. Differenitations in the request methods can be used via built in features or from further programming to map the APIs to its proper functionality correctly. 

## HEAD => GET

The HEAD request is now a relec of the past. Prior to the 2000's was common for users to ask for the headers of a request to see if they wanted to take on the burden of recieving the data from the request because of bandwidth issues. In recent history, developers stopped writing HEAD requests, but users still wanted access to this option. Hence, a feature was added to backend web frameworks that is hidden and undiscussed: HEAD requests get automatically mapped to GET requests. Now, developers did not have to worry about writing the HEAD API but end users still had access to the headers without returning the data! This appears to be a win-win scenario for everyone. 

## Testing Outline

Many developers write logic based upon the **method** of request that is sent. This was the question that I asked myself: *"Would it be possible to abuse this obscure logic to bypass security features?"* If developers do not know about this feature of their service then they might write logic that is vulnerable to a security bypass. 

It was time to discover which frameworks were vulnerable to these types of attacks. This is the test plan I went with: 
- Test all HTTP verbs being sent to a service to see what happens. Use following verbs for each test configuration: GET, POST, PUT, PATCH, DELETE, CONNECT, OPTIONS, HEAD, TRACE, ?? (invalid)
- Test a plethora of backend web frameworks. 
    - The following frameworks were tested: Django, Flask, Ruby on Rails, Springboot, Larvel, Express and ASP.net. 
    - With all of these services, test them in the different ways that a web server can be setup. For testing, this included non-standard setups that are still available within the framework. 

## Impact

What does this bug actually mean for security? I thought that clarifying this before reading the application specific bugs would be useful. The most common attack vector is bypassing CSRF token checks. CSRF is an attack that forces a user to make unintended state changing actions on a website. In order to prevent this attack, random tokens are added to state-changing requests. Most web frameworks automatically check for CSRF tokens on all requests that change state (POST, PUT, PATCH, DELETE, etc.). So, if the logic for a POST request (or any state changing method) can be triggered on an endpoint, without actually making a POST request, this would bypass the CSRF token check while making the state changing request. This is a direct compromise in the security of the application, as it defeats the CSRF protection of that API. The following example, in Flask, shows this type vulnerability off: 

<----Picture/Code---->
@app.route("/unsafe", methods=["GET", "POST"])
def log_in_unsafe():

    if(request.method == "GET"):
        print("GET")
        return "GET"
    else:
        print("POST")
        return "POST" 
<-------------------->

In the code shown above, a GET request would hit one endpoint, while POST would hit another. Also, in this scenario, a HEAD request would hit the else clause! This is because the request assumes that if the request is a GET or a POST, and does not take into consideration that a HEAD request could hit this code path. It should be noted that a HEAD request would not trigger a CSRF token check. So, a cross-site HEAD request on this API would be able to hit the state changing actions, bypassing the necessary CSRF token check. 

## Findings 

Below, the results of 7 backend web frameworks will be discussed. In particular, this will talk about the different potential setups for a framework and the likehilihood of a logic bypass. 

### Flask 

Flask is a lightweight web application framework that is built upon Python. It is quite popular, especially because of how easy it is to get started with Flask. 

In Flask, the default configuration allows for all *methods* to be used on an API. The request can be filtered down in two ways: checking the request method in a global variable or specifying the methods allowed on an API with function decorators. 

It should be noted that all HEAD requests are mapped to GET requests in Flask.

#### Attacking Flask 

From the research, all Flask HEAD requests will get mapped to GET requests, even when only a GET request is specified in the allowed request types. Because Flask allows for multiple request methods for a specific endpoint, a developer could easily write code that expects only a GET or POST request. So, the logic could be built in this way, defaulting to the POST request (such as the example in the **Impact** section described above). By using a HEAD request, the CSRF token check could be bypassed and would trigger the state changing functionality. 

### Django 

Django is another Python based web application framework. Django takes security very seriously, is very scalable and is also opionioned aboutå design choices. 

In Django, there were two main configurations are that are used for API endpoints: function level and class based views. Both of these configurations had differnt perks so they will be discussed seperately. 

The function based (most common) defaults to not restricting the request method. With this setup, all requests are sent to a single API for a given route. An additional feature of this configuration, is that decorators can be added in order to restrict the request method being used on the API. The request method does very strict checks on on the type of request being used. So much so that not even a HEAD request will map to a GET request in this setup. 

The class based views (less common) use a more traditional REST API model. This means that there is a single request method per function on a given URL endpoint. 

The HEAD request was only mapped to GET in the class-based view configuration, while the decorators (in the function based view) did not add the HEAD request method to a GET request. 


#### Attacking Django

In the function based routing, there are potential routing problems. A developer might assume that only GET requests are being used for one part of the service and just allow all others (POST PATCH, PUT ) for another part of the service. By using a HEAD request, it would be possible to hit the other functionality, without passing the CSRF token check. Of course, this attack only works when the request method is not specified for a given endpoint in the function based views.

### Express

Express is a backend web framework that is written in JavaScript. This is used by teams who want to use a single language when developing both the frontend and the backend application. 

Express uses a REST based model for all requests. So, each IRL endpoint must specify what type of HTTP method it is accepting.

Additionally, there is a request that accepts all endpoints: *app.all*. 

It should be noted that the HEAD request was always sent to GET requests. 

#### Attacking Express 
The same as Django. The key understanding is that all request methods go to the same API with the *.all* request type. 


### Ruby on Rails

Ruby on Rails is an MVC Ruby based web application framework. Ruby allows for very fine grained control of most things and is very verbose. 

The routing, in Ruby on Rails, is very interesting to the developer. Out of all the frameworks discussed, this gives the most fine-grained control over which routes get mapped to what endpoints. In fact, there is a special file that controls the routes within a given part of the website. 

Ruby on Rails maps all HEAD requests were mapped to the GET requests for a given endpoint. 

#### Attacking Ruby on Rails 

There are two main scenarios: all request methods go to a single endpoint and request mapping to only specific request methods to a given endpoint. 

In the first scenario (all => one endpoint), the attack situation is the same as both Express and Django (the all method).

In the second scenario, a developer would only expect the specified request methods to be used on a given endpoint. However, because HEAD requests are mapped to GET requests, there could be a bypass in the discussed logic. This attack ends up being the same as Flask described above. 

### Laravel 

Laravel is a PHP based web framework that includes a lot of default features. 

The routing comes in a standard REST API setup that has a single request method endpoint to a single API. There is also an 'any' route within Laravel, that maps all request types to a given endpoint. 

It should be noted that all HEAD requests are mapped to GET requests. 

#### Attacking Laravel 
Same as Express and Django with the *.all* method being exploitable, if not setup correctly. 

### ASP.NET 

ASP.net is a Microsoft web framework that is written that uses C#. ASP.net is cross platform and is quite versititle. ASP.net takes security very seriously! In fact, they are the only service that defaults to using HTTPs instead HTTP locally. 

ASP.net defaults to having a single request method map and URL to a single function. However, endpoints can be changed to accept more than one request method per call. 

It should be noted that **NO** HEAD requests are mapped to GET requests. This was the only framework of the 7 tested that was found to not have this functionality at all. 

#### Attacking ASP.NET 

Two major items make ASP.NET not an interesting thing to attack: HEAD is not mapped to GET and there are no *all* request method requests. 
In theory, a developer could setup an API endpoint that manually specifies all request types, then bulid poor logic (similar to Express,Django and Laravel) that would be exploitable. But, in most circumstances, ASP.net is completely safe from the attacks described above. 


### Springboot 

Springboot is an open source Java based framework, mainly used for Microservices. 

Springboot uses a REST based model, where explicit request types have to be specified. However, it is possible to specify multiple request methods per endpoint with function decorators. 

All HEAD requests are automatically mapped to GET requests with Springboot.

#### Attacking Springboot

Springboot maps HEAD requests to GET requests and has the abiilty to specify multiple requests methods per endpoint. So, it is likely that a developer would write some logic for a GET request and other logic for everything (POST,etc.). Hence, this attack would be similar to those performed on Flask and some configurations of Ruby on Rails. 

## Conclusion

Writing logic based upon the request method can be difficult, particularly when the framework is adding in unexpected request mapping. Regardless, several frameworks are more vulnerable to this than others. 

Why? Developers who are using the 'all' method on an API are less likely to write if-else logic because items such as PUT, POST and other request methods could be used to invoke unintended logic. But, because several frameworks automatically do CSRF checks, a developer may specify an action for a GET (no CSRF check) and one for everything else (with CSRF check). These frameworks are still potentially vulnerable to poorly written code but appear more wholesome than others. Every one of the aforementioned frameworks besides ASP.net falls into this category. 

The frameworks that are the most deceiving are the ones that allow for specific request methods for a given endpoint and still allow HEAD requests to hit the endpoint. Which frameworks fell into this category? Some configurations of Ruby on Rails, Springboot and Flask. Because of this, developers are much more likely to make programmatic routing mistakes in these frameworks that could lead to a CSRF bypass. 

Subtle bugs can be in code bases for years without being discovered. By unearthing obscure features of frameworks we can conquer these types of bugs. In this article had two main insights: developers write code to manually handle requests based upon the request method and HEAD requests are automatically mapped to GET requests APIs. Using these two features together can be used to bypass the security of applications; be on the look out for these in the future. 

## References 
- The originally article that inspired this deeper research was by Teddy Katz. He found a CSRF bug in Github (used Ruby on Rails at the time) that abused the topic of this article. The original blog post can be found at https://blog.teddykatz.com/2019/11/05/github-oauth-bypass.html. 
- CSRF explanation: https://owasp.org/www-community/attacks/csrf


