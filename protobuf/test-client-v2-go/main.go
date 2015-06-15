package main

import (
    b64 "encoding/base64"
    "log"
    "net"

    "github.com/golang/protobuf/proto"
    "../compiled_v2"
)

func get_message() (*chatroom.Message) {
    user := &chatroom.User {
        Id: proto.Int32(1),
        Email: proto.String("xyz@localhost"),
        Username: proto.String("test-user"),
        FirstName: proto.String("Frank"),
        LastName: proto.String("Underwood"),
        Age: proto.Int32(50),
    }
    room_type := chatroom.RoomType_PUBLIC
    room := &chatroom.Room {
        Id: proto.Int32(2),
        Name: proto.String("test room"),
        Type: &room_type,
    }
    message := &chatroom.Message {
        Id: proto.Int32(3),
        User: user,
        Room: room,
        Msg: proto.String("test message"),
    }

    return message
}

func send(data []byte) {
    conn, err := net.Dial("tcp", "localhost:8002")
    if err != nil {
        log.Fatal("net.Dial error: ", err)
    }

    b64_data := b64.StdEncoding.EncodeToString(data)

    conn.Write([]byte(b64_data))
    log.Println("data sent")
}

func main() {
    log.Println("Hello")

    message := get_message()
    data, err := proto.Marshal(message)
    if err != nil {
        log.Fatal("marshalling error: ", err)
    }
    log.Println("data: ", data)

    send(data)
}
