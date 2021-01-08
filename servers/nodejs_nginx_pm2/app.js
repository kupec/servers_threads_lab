const http = require('http');

http.createServer((req, res) => {
    setTimeout(() => {
        res.end('GOOD');
    }, 100);
}).listen(3000);
