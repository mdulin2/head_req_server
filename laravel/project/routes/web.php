<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    error_log('GET');
    return "GET";
});
Route::post('/', function () {
    error_log('POST');
    return "POST";
});
Route::put('/', function () {
    error_log('PUT');
    return "PUT";
});
Route::patch('/', function () {
    error_log('PATCH');
    return "PATCH";
});
Route::delete('/', function () {
    error_log('DELETE');
    return "DELETE";
});

// This route is vulnerable to the request presumption here. According to some docs, people actually use this functionality. 
Route::any('/unsafe', function () {
    error_log(Request::method());
    if(Request::method() == "GET"){
        error_log("GET"); 
        return "GET";
    }

    // Use for a POST request (in theory) 
    else{
        error_log("Other request!"); 
        return "Other";
    }

}); 

