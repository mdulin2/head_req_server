class ApplicationController < ActionController::Base
    skip_before_action :verify_authenticity_token
    protect_from_forgery with: :exception # Add this for the CSRF testing.
    
    def index 
        @request_type = request.method_symbol
        puts(@request_type)

        case @request_type
        when :get 
            puts("GET")
            render plain: 'GET'
        when :post 
            puts("POST") 
            render plain: 'POST' 
        when :patch 
            puts("PATCH")
            render plain: 'PATCH'
        when :delete 
            puts("DELETE") 
            render plain: 'DELETE'
        when :put 
            puts("PUT") 
            render plain: 'PUT' 
        else 
            puts(@request_type)
            render plain: @request_type
        end 
    end 

    ## The request specific calls 
    def GET 
        puts('GET')
        render plain: 'GET'
    end 

    def POST 
        puts('POST')
        render plain: 'POST'
    end 

    def PATCH 
        puts('PATCH')
        render plain: 'PATCH'
    end 

    def PUT 
        puts('PUT')
        render plain: 'PUT'
    end 

    def DELETE 
        puts('DELETE')
        render plain: 'DELETE'
    end 

    # The particularly unsafe call. 
    # This is because the request type is only checked if it is a GET and then assumes that it is a POST otherwise. 
    def unsafe
        @request_type = request.method_symbol

        # Makes the assumption that only GET and POST requests can be here, even though HEAD can also hit this endpoint
        if(@request_type == :get)
            render plain: 'GET' 
        else # Shold only be POST 
            puts('Bypass CSRF check by using a HEAD request')
            render plain: 'POST <--Done by a bad implicit assumption'
        end
    end
end
