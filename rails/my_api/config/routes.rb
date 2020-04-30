Rails.application.routes.draw do
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  match '/', to: 'application#index', as: :index, via: :all

  get '/spec' => 'application#GET'

  post '/spec' => 'application#POST'

  put '/spec' => 'application#PUT'
  
  patch '/spec' => 'application#PATCH'

  delete '/spec' => 'application#DELETE'

  # Unsafe one... 
  match "unsafe" => "application#unsafe", via: [:get, :post]
end
