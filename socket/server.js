const path = require('path');
const http = require('http');
const express = require('express');
const app = express();
const formatMsg = require('./util/messages');
const bot = "Server";

const server = http.createServer(app);
const io =require('socket.io')(server)

app.use(express.json());
app.use(express.urlencoded({ extended:true }));
app.use(express.static(path.join(__dirname, 'public')));



io.on('connection', socket =>{
    socket.emit('message', formatMsg(bot, "Hello"));

    socket.broadcast.emit("message", formatMsg([bot, 'A user has connected']));

    socket.on('disconnect', () =>{
        io.emit('message', formatMsg([bot, 'A user has left']));
    });

    socket.on('chatMessage', (msg)=>{
        io.emit('message', formatMsg(msg))
   })
    
});

const port = 3000 ||process.env.PORT;

server.listen(port, () =>{
    console.log(port);
});

