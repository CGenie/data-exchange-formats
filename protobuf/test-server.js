var net = require('net');
var fs = require('fs');
var ProtoBuf = require('protobufjs');

// "builder" contains all message types defined in chatroom.proto|desc.
var builder;
var version;
if(process.argv[2] == 'v2') {
    builder = ProtoBuf.loadProtoFile('chatroom-2.proto');
    version = 2;
} else {
    builder = ProtoBuf.loadProtoFile('chatroom.proto');
    version = 1;
}


// The "chatroom" package.
var chatroom = builder.build('chatroom');

var server = net.createServer(function(c) {  // 'connection' listener
    console.log('client connected');
    c.on('end', function() {
        console.log('client disconnected');
    });
    c.on('data', function(data) {
        var msg;

        console.log('--------------------------------');
        console.log('Incoming data: ', data.toString());

        msg = chatroom.Message.decode(data.toString(), 'base64');
        console.log('unserialised:', msg);
    });
});

server.listen(8002, function() {
    console.log('server bound, version', version);
});