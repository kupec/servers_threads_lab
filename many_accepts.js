const os = require('os');
const http = require('http');
const net = require('net');
const {fork} = require('child_process');

if (!process.env.SLAVE) {
    const server = net.createServer().listen(3001);

    for (let i = 0; i < os.cpus().length; i++) {
        const worker = fork(__filename, [], {
            env: {
                SLAVE: 100+i,
            },
            stdio: [0, 1, 2, server._handle.fd, 'ipc'],
        })
    }

    server.close();
}
else {
    const answer = "GOOD: " + process.env.SLAVE; 
    http.createServer((req, res) => {
        setTimeout(() => {
            res.end(answer);
        }, 100);
    }).listen({fd: 3});
}

