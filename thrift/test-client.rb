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
user.email = 'president@whitehouse.gov'
user.username = 'MrPresident'

if version == 2 then
    user.firstName = 'Frank'
    user.lastName = 'Underwood'
    user.age = 50
    user.badges = ['caring', 'loving']
    user.after_badges = 'after badges'
end

room = Room.new
room.id = 2
room.name = 'Chat with Claire'
room.type = RoomType::PRIVATE

message = Message.new
message.id = 3
message.user = user
message.room = room
message.timestamp = Time.now.getutc.to_i
message.msg = 'Hello Honey'

puts 'Serialized: ', serializer.serialize(message)

s = Socket.new Socket::AF_INET, Socket::SOCK_STREAM
s.connect Socket.pack_sockaddr_in(8003, '127.0.0.1')
s.puts serializer.serialize(message)
