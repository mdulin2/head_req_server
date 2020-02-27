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

## Targets 
- ~~Django~~
- ~~Flask~~ 
- Ruby on Rails 
- ~~Express~~
- ~~Springboot~~
- ~~ASP.net~~
- ~~Laravel~~

## Findings 
- The real bypass for these types of attacks is finding a request that bypasses the CSRF checks (HEAD, OPTIONS and GET do not require these in lots of frameworks) to perform state changing actions. It appears that a simple check for GET then the else statement is not enough. 

## Knowledge/Tested
- Ruby on Rails: 
  - Maps HEAD to GET automatically (https://blog.teddykatz.com/2019/11/05/github-oauth-bypass.html) 
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
- Overall: 
  - Ruby on Rails, Django (in some normal configurations) and Flask are vulnerable to this issue. 
  - Express, Laravel and Springboot are potentially vulnerable if a specific setup for the API is used. 
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

### Flask 
  - By default, the listener listens for a GET request. This GET listener also accepts HEAD requests too. 
  - With a specific allowed method types on a request (i.e., use GET and POST) the HEAD request is assumed to be added with a GET request. 
  - /login-unsafe shows an example where the GET method is assumed and uses a HEAD request, even though this is not specified. 
  - Even with an empty allowed methods, the OPTIONS is still allowed. 
  - If an invalid request type is given, then the request just assumes that the request type is not allowed (405 response). 
  - Flask does not do automaticly CSRF token checks. So, the usage of HEAD on top of a GET request does not make much of a difference (likely). But, this is still good to know!
  - The options request does not actually trigger the execution of the function. However, a HEAD request does.

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

## Laravel 
  - Has built in CSRF protection on requests that are not GET requests? 
  - Uses a REST based model. So, all of the requests methods are separate 
  - HEAD requests are mapped to GET requests, by default. 
  - However, there is still an 'any' route that can (and does get used) at times. 
    - The any route is vulnerable to this implicit assumption attack, as demonstrated in the demo code. 
  - The main source code is in /routes/web.php




