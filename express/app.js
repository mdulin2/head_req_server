/*
Install nodejs 
Install express via npm 

By default, the listens on http://127.0.0.1:3000
*/

const express = require('express')
const app = express()
const port = 3000

// Works for both HEAD and GET
app.get('/', (req, res) =>{
    console.log('GET')
    res.send('Get!');
});

app.all('/vuln', function (req, res, next) {
    if(req.method == "GET"){
        // Do xyz
    }

    // Implicit assumption about the POST request being used after a CSRF token check...
    // A head request would hit this point (depending on the configurations of the CSRF protections on the site)
    else{
        console.log("Potentially vulnerable! Req: " + req.method);
    }

    res.send('All!')
});


// If only the post request, then ONLY post is allowed. 
app.post('/', (req, res) =>{
    console.log('post')
    res.send('Post!');
});

app.put('/', (req, res) =>{
    console.log('put')
    res.send('Put!');
});

app.patch('/', (req, res) =>{
    console.log('patch')
    res.send('Patch!');
});

app.delete('/', (req, res) =>{
    console.log('delete')
    res.send('Delete!');
});

/*
app.head('/', (req, res) =>{
    console.log('head')
    res.send('Head!');
});
*/


app.listen(port, () => console.log(`App listening on port ${port}!`));