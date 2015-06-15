var net = require('net');
var fs = require('fs');
var ProtoBuf = require('protobufjs');

// "builder" contains all message types defined in chatroom.proto|desc.
var builder = ProtoBuf.loadProtoFile('chatroom.proto');
var builder_v2 = ProtoBuf.loadProtoFile('chatroom-2.proto');

// The "chatroom" package.
var chatroom = builder.build('chatroom');
var chatroom_v2 = builder_v2.build('chatroom');

var server = net.createServer(function(c) {  // 'connection' listener
    console.log('client connected');
    c.on('end', function() {
        console.log('client disconnected');
    });
    c.on('data', function(data) {
        var msg;

        console.log('--------------------------------');
        console.log('Incoming data: ', data.toString());

        try {
            msg = chatroom_v2.Message.decode(data.toString(), 'base64');
            console.log('unserialised (v2):', msg);
        } catch(e) {
            msg = chatroom.Message.decode(data.toString(), 'base64');
            console.log('unserialised:', msg);
        }
    });
});

server.listen(8002, function() {
    console.log('server bound');
});