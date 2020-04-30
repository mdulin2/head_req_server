# Request Handling Based Upon Methods

## Introduction 

Some security issues are quite obvious and easy to find based upon very simple patterns. However, there are others that lie deep below the surface, stemming from developers not understanding the technology they were using.

Today, I wanted to share another item to add to the tool belt. This bug comes from two main insights: developers can programmatically route requests based upon request methods and some backend servers automatically map *HEAD* requests to *GET* requests. The next few sections will dive into *how* these features can be used bypass security mechanisms. Finally, we will see which backend web frameworks are potentially vulnerable to this type of attack. This post was inspired by a Github vulnerability that was discovered via this very technique [3].

## Request Types 

The HTTP protocol has a set of **request** methods that allow/describe the action to be performed on a resource. These *methods* are commonly referred to as HTTP verbs. All of these verbs have their own purpose. For this post, there are three main verb categories we will talk about: 
- GET 
- HEAD 
- State Changing Verbs (POST, PUT, DELETE, PATCH) 

The *GET* verb justs *gets* data for the user. A *HEAD* request is exactly the same as a *GET* request except that no data is returned to the user; only the headers are returned from the request. Finally, several requests are only for altering data in some capacity(POST, PUT, DELETE and PATCH). For the purpose of this article, no other information is needed, as it is irrelevant for the findings. If you would like to learn more about the different request methods, please visit [1].

## Request Mappings 

When creating API's, the proper functionality is chosen based upon the *URL*, *URL parameters* and the *request method*. Differenitions in the request methods can be used via built in features or from further programming to map the APIs to its proper functionality correctly. 

### HEAD => GET

An interesting case of *request mapping*, is the the *HEAD* request. In recent history, developers stopped writing HEAD requests, but users still wanted access to this option. Hence, a feature was added to backend web frameworks that is hidden and undiscussed: HEAD requests get automatically mapped to GET requests. This appears to be a win-win scenario for everyone, but most developers do not know about this. 

## Testing Outline

Many developers write logic based upon the **method** of request that is sent. This was the question that I asked myself: *"Would it be possible to abuse this obscure logic to bypass security features?"* If developers do not know about this feature of their service then they might write logic that is vulnerable to some type of security bypass. 

This is the test plan I went with for the research to discover where this could potentially be exploited at:
- Test all HTTP verbs being sent to a service to see what happens. Use following verbs for each test configuration: 
    - GET, POST, PUT, PATCH, DELETE, CONNECT, OPTIONS, HEAD, TRACE, ?? (invalid)
- Test a plethora of backend web frameworks. The following frameworks were tested:
    -  Django, Flask, Ruby on Rails, Springboot, Larvel, Express and ASP.net. 

NOTE: With all of these services, test them in the different ways that a web server can be setup. For testing, this included non-standard setups that are still available within the framework. 

## Impact

What does this bug actually mean for security? I thought that clarifying this before reading the application specific bugs would be useful. The most common attack vector is *bypassing CSRF token* checks. CSRF is an attack that forces a user to make unintended state changing actions on a website. In order to prevent this attack, random tokens are added to state-changing requests. Most web frameworks automatically check for CSRF tokens on all requests that change state (POST, PUT, PATCH, DELETE, etc.). For more information on CSRF, please refer to [4]. 

If the **logic** for a POST request (or any state changing method) can be triggered on an endpoint, without actually making a POST request, this would bypass the CSRF token check while making the state changing request. This is a direct compromise in the security of the application, as it defeats the CSRF protection of that API. The following example, in Flask, shows this type vulnerability off: 

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

In the code shown above, a GET request would hit one endpoint, while POST (or anything else) would hit another. The key insight is that (in Flask), HEAD requests are automatically mapped to GET requests. Because of this, a HEAD request would hit the POST part of the endpoint! This is because the request assumes that if the request is a GET or a POST, and does not take into consideration that a HEAD request could hit this endpoint. Most importantly, it should be noted that a HEAD request would not trigger a CSRF token check. So, a cross-site HEAD request on this API would be able to hit the state changing actions, bypassing the necessary CSRF token check. 

## Findings 

The likeihood of a configuration being exploited can be broken down into two categories: Directly Mapped APIs and All Requests. 

### Directly Mapped 

Several frameworks allow for multiple request methods to map to the same endpoint. In this situation, it is very common for functionality to be choosen based upon the request method. 

When the developer can specify which request methods are allowed on an endpoint and this is not exactly followed, it can lead to logic bugs. Flask, Springboot and some configurations of Ruby on Rails were found to be vulnerable to this attack if configured improperly. An example of a vulnerable configuration can be seen in the Flask example shown above. 

### Accept All Methods 

Several frameworks have an endpoint that will accept all HTTP methods. For some framworks, this is the only way that the framework actually works. 

When developers create logic, based upon these request methods, mistakes can be made that lead to logic bugs. A developer could write code similar to the following: 
```
def index(request): 
    if(request.method == 'GET'):
        print("do GET stuff")
    else: 
        print("Do other stuff")
    return HttpResponse(str(request.method))
```

In the above Django example, the developer is assuming that only a GET request can hit this endpoint **and** pass the CSRF check. By making a non-GET request that still bypasses the CSRF check, this can trigger an unintended function call. What is considered a *safe* request? According to RFC 7231 [3], GET, HEAD, OPTIONS and TRACE are *safe* requests that do not require CSRF tokens validation. The results section has a *table* showing the results of each request method for each framework and how it handles CSRF token checks. 

It should be noted that this situation does not rely on HEAD requests being mapped to GET. However, it does rely on the fact that HEAD requests do not get checked for CSRF tokens. 

## Results Tables 

The following table shows the findings from the research: 
```
Frameworks tab inside of `TableOfMappings.xlsx`
Framework -- Directly Mapped -- Accept All Endpoints -- Map Head to GET
--------------
```

None of these result in a vulnerability directly. However, the logic of the routing, built into the framework, can result in unexpected cases.  
It should be noted that this table is not exhaustive. Several of the frameworks support multiple ways to do routing. This table just shows a yes/no result for whether the frameworks have this functionality, in any capacity. For more into this, please visit the in-depth report/notes at [5].

The following table demonstrates which request methods do not validate CSRF tokens for each framwork:

```
CSRF_NOT_CHECKS tab inside of `TableOfMappings.xlsx`
```

Most of the frameworks were as strict or stricter than the specification. However, Flask was the lone framework that was not in this category; it also allows for the CONNECT verb and invalid verbs (?) to bypass CSRF token checks, if explicitly stated. 


## Conclusion

Writing logic based upon the request method can be difficult, particularly when the framework is adding in unexpected request mapping.

Subtle bugs can be in code bases for years without being discovered. By unearthing obscure features of frameworks we can conquer these types of bugs. In this article had two main insights: developers write code to manually handle requests based upon the request method and some frameworks automatically map HEAD requests are automatically mapped to GET requests APIs. Using these two features together (or the first way by itself) can be used to bypass the security of applications.

## References 
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods. 

- RFC spec: https://tools.ietf.org/html/rfc7231.html#section-4.2.1
- https://blog.teddykatz.com/2019/11/05/github-oauth-bypass.html. 
- https://owasp.org/www-community/attacks/csrf
- In depth notes, with examples from research, at Github. TBD.

