#!/usr/bin/env ruby

$:.push('gen-rb')

require 'thrift'

version = 1
if ARGV[0] == 'v2' then
    version = 2
    require 'chatroom_2_types'
else
    require 'chatroom_types'
end

puts 'Hello, version', version

transport = Thrift::MemoryBufferTransport.new()
protocol = Thrift::BinaryProtocol.new(transport)
serializer = Thrift::Serializer.new

transport.open

user = User.new
user.id = 1
user.email = 'xyz@localhost'
user.username = 'test-user'

if version == 2 then
    user.firstName = 'Frank'
    user.lastName = 'Underwood'
    user.age = 50
    user.badges = ['novice', 'intermediate']
end

room = Room.new
room.id = 2
room.name = 'test room'
room.type = RoomType::PUBLIC

message = Message.new
message.id = 3
message.user = user
message.room = room
message.msg = 'test message'

puts 'Serialized: ', serializer.serialize(message)

s = Socket.new Socket::AF_INET, Socket::SOCK_STREAM
s.connect Socket.pack_sockaddr_in(8003, '127.0.0.1')
s.puts serializer.serialize(message)
