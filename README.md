## Request Differences
Some web frameworks automatically map HEAD requests to GET. I am curious how wide-spread this is. Additionally, I am cuious if any other frameworks map any other types of requests to anything else.   

I noticed this was weird aafter reading the ruby on rails article about Github. So, I thought that I would test this out myself!

So, we will be testing the following requests types: 
- get 
- post 
- put 
- patch 
- delete 
- connect 
- options 
- head
- trace 
- ?? (invalid)

## Random 
- python requests: 
  - Does not support TRACE, TRACK, CONNECT or invalid. 
  - Had to use CURL in order to test this
- Run the test script: 
  - python3 tester.py (needs to be python3 because of the call to subprocess)

## Setup 
- django 
  - Install django dependencies 
  - python3 manage.py runserver
- Flask 
  - Install flask dependencies 
  - python3 main.py
- Express 
  - Install node and expressjs 
  - node app.js
- Springboot: 
  - This is NOT my project. I borrowed this setup for terms of the demonstration. 
  - https://spring.io/guides/gs/actuator-service/ 
  - ./gradlew clean build -x test && java -jar build/libs/actuator-service-0.0.1-SNAPSHOT.jar in the complete directory 
  - My setup runs on port 9000. This may change for you depending on the setup. 
- ASP.net: 
  - Use visual studio (free edition works fine) 
  - The web server runs on https://127.0.0.1:5001/weatherforecast by default. 
- Laravel 
  - Install using Composer 
  - Use PHP 7.2 or greater for this application
  - Run `php artisan serv` to turn on the API.
- Ruby on Rails: 
  - Install Ruby on rails 
  - Run ``rails s`` to start the service 
  - It runs on http://localhost:3000

## Targets 
- ~~Django~~
- ~~Flask~~ 
- ~~Ruby on Rails~~ 
- ~~Express~~
- ~~Springboot~~
- ~~ASP.net~~
- ~~Laravel~~

## Findings 
- The real bypass for these types of attacks is finding a request that bypasses the CSRF checks (HEAD, OPTIONS and GET do not require these in lots of frameworks) to perform state changing actions. It appears that a simple check for GET then the else statement is not enough. 

## Knowledge/Tested
- Flask:  
  - Maps HEAD to GET automatically (https://stackoverflow.com/questions/22443245/why-does-apache-wsgi-map-head-to-get-how-to-speed-up-head-in-flask). 
  - Does not specify which request type must be used. So, because HEAD is mapped to GET, this is vulnerable. 
- Django: 
  - Maps HEAD to GET with class based views (if HEAD is not implemented). 
  - With the normal usage, if a decorator is explicitly set to use GET or POST, the HEAD request will not work. However, if no request type is specificed, then the HEAD will work as a GET request. 
  - This is vulnerable in lots of configurations
  - View the Django below for more information. 
- Express: 
  - Each request type has to be explicitly stated. 
  - app.all may also be used for this. Vulnerable in this configuration.
- Springboot:
  - Each request type has to be explicitly stated, but an API can accept multiple. 
  - Maps HEAD to GET requests. 
  - This is vulnerable in certain configurations. 
- ASP.NET: 
  - No implicit request assumptions! But even HEAD requests are mapped to GET. All of these have to be specifically stated. 
- Laravel 
  - Makes the implicit assumption of HEAD requests to GET requests.
  - The ANY request type is vulnerable to these types of attacks. 
- Ruby on Rails: 
  - Maps HEAD to GET in all circumstances
  - Vulnerable to the attack described above. 
- Overall: 
  - Ruby on Rails, Springboot, and Flask are vulnerable to this issue. 
  - Django, Express and Laravel are potentially vulnerable if a specific setup for the API is used. 
  - ASP.NET does a great job protectioning against this issue! :) So, it is not vulnerable. 

## Tested Content Servers 
### Django: 
  - Some requests view the request type manually:
    - The CSRF token check is done at the framework level and not at the function level. So, CSRF token bypasses are really interesting. 
    - So, this accepts **all request types**. A check for GET (while head is there) will work just the same. 
    - If an added decorator only allows for a specific method, (GET) then the HEAD request is not allowed in this case. 
    - This will even accept invalid HTTP request types such as '?'.
  - However, there is something called 'class based views'. 
    - Most things are denied by default, if the method is not implemented. 
    - In django, all requests are allowed besides connect if they are created within the class based view. 
    - Otherwise, the request is not allowed. 
    - The HEAD request is mapped to the GET request if the HEAD request was not defined. 
  - CSRF Checks: 
    - On all but GET, HEAD, OPTIONS, TRACE. This is directly according to the HTTP spec as 'safe' methods: https://tools.ietf.org/html/rfc7231.html#section-4.2.1

### Flask 
  - By default, the listener listens for a GET request. This GET listener also accepts HEAD requests too. 
  - With a specific allowed method types on a request (i.e., use GET and POST) the HEAD request is assumed to be added with a GET request. 
  - /login-unsafe shows an example where the GET method is assumed and uses a HEAD request, even though this is not specified. 
  - Even with an empty allowed methods, the OPTIONS is still allowed. 
  - If an invalid request type is given, then the request just assumes that the request type is not allowed (405 response). 
  - Flask does not do automaticly CSRF token checks. So, the usage of HEAD on top of a GET request does not make much of a difference (likely). But, this is still good to know!
  - The options request does not actually trigger the execution of the function. However, a HEAD request does.
  - CSRF: 
    - Depends on the way that the service is being used. FlaskForm automatically does CSRF token checks. 
    - Otherwise, it can be imported in.
    - Methods where CSRF is not checked: GET, HEAD, TRACE, CONNECT and '??'. The verb MUST be specified, in order for this to work. 
    - NOTE: OPTIONS does not make the API do anything. 
    
## Express 
  - For a GET request, the HEAD is automatically added to this request. 
  - An invalid HTTP request type gives a 400 error for a bad request. 
  - Connect connects, then gives an empty reply from the server (how this is supossed to work) 
  - OPTION returns the allowed HTTP methods (as expected). When a GET request is added, the HEAD is added as an option too. 
  - Each request method has to be explicitly set for a given route. So, using this technique for express is not very interesting. 
  - There is also a special request type of ``app.all`` that can be called: 
  - When using this, you can even modify the options request. 
  - The HEAD request will not return any response, even if you attempt to return something.
  - The invalid request type does not get mapped to anything. 
  - Connect is not affected by this. 
  - CSRF Tokens: 
    - Have to add explicit middleware for CSRF tokens. 
    - ex: https://github.com/expressjs/csurf
    - NOTE: CONNECT does not make the API do anything. But, OPTIONS does. 

## Springboot 
  - By default (with a normal GET server) HEAD is automatically mapped to the GET request. 
  - Most SpringBoot stuff is going to use MVC on the backend (REST). So, this is what the rest of the testing should probably use. 
  - An invalid HTTP request ('??') causes the server to error out. 
  - Connect does not work by default with this setup (uses Apache Tomcat) 
  - CSRF protection has to be explicitly turned on with Springboot.
  - Because the REST is used, this server is not vulnerable to attacks of the implicit assumptions.
  - A single route can use **multiple** HTTP methods. So, using this, a route could be vulnerable to this attack. 

## ASP.NET 
  - By default, the API package uses a REST based model. 
  - Does not automatically map HEAD to GET. They have to be specifically specified! 
  - Only web server to use HTTPS on the local system, by default. 
  - The dynamic route mapping for ASP.NET should not matter because HEAD requests are not even mapped to GET requests. 
  - Can use the **AcceptVerbs** function. But, these need to be explicitly stated in order to use these methods. 
  - CSRF -- On by default for Razor pages. Everything else, it has to be manually created and added (uh oh) 
    - This boilerplate site has an interesting thought... 
      - https://aspnetboilerplate.com/Pages/Documents/XSRF-CSRF-Protection 
      - By default, only POST, PUT, PATCH and DELETE have anti-CSRF protections 
## Laravel 
  - Has built in CSRF protection on requests that are not GET requests/HEAD
  - Uses a REST based model. So, all of the requests methods are separate 
  - HEAD requests are mapped to GET requests, by default. 
  - However, there is still an 'any' route that can (and does get used) at times. 
    - The any route is vulnerable to this implicit assumption attack, as demonstrated in the demo code. 
  - The main source code is in /routes/web.php
  - CSRF is turned on by default: 
    - These methods do not triger a CSRF token check: OPTIONS (returns data for some reason), GET, HEAD (no data returned) and TRACE causes an error (not CSRF error).
    - NOTE: CONNECT does not trigger the requests, but is accepted as a request. 

## Ruby on Rails 
  - Protects from CSRF by default! Have to add a directive to remove the check entirely. 
  - Handling multiple requests incorrectly: 
      - https://stackoverflow.com/questions/5583707/how-to-handle-multiple-http-methods-in-the-same-rails-controller-action 
  - Routing: 
      - Very unique! 
      - Can specify per verb or to map all of a particular type to a request  
  - Mapping all to a given route: 
      - All verbs are treated as equal and nothing interesting happens. 
  - Map specify requests to a route (i.e post and get): 
      - A head request is set onto the GET, even though CSRF protections are completely turned off for this. 
      - This **is** a security issue if implicit assumptions are made about the type of request being used. 
  - If using verb specific calls, HEAD gets mapped to GET. 
  - The other types of requests (connect and trace) just don't do much 
  - ?? (invalid) returns an error message about an improper request being used
  - CSRF checks have to be added in with a flag: 
    - All requests, besides the following, require a CSRF token... GET and HEAD. Even CONNECT, OPTIONS and TRACE need one. 



