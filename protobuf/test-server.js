var net = require('net');
var fs = require('fs');
var ProtoBuf = require('protobufjs');

// "builder" contains all message types defined in chatroom.proto|desc.
var builder = ProtoBuf.loadProtoFile('chatroom.proto');
console.log('builder', builder);

// The "chatroom" package.
var chatroom = builder.build('chatroom');
console.log('chatroom', chatroom);

//var ob = { num: 42 };
//ob.payload = new Buffer("Hello World");

//var proto = BufTest.serialize(ob);
//console.log('proto.length:', proto.length);

var server = net.createServer(function(c) {  // 'connection' listener
    console.log('client connected');
    c.on('end', function() {
        console.log('client disconnected');
    });
    c.on('data', function(data) {
        console.log('Incoming data: ', data.toString());
        debugger;

        var msg = chatroom.User.decode(data.toString(), 'base64');
        console.log('unserialised:', msg);
    });
});

server.listen(8002, function() {
    console.log('server bound');
});