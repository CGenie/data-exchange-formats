/* Specification of a simple chatroom protocol */

typedef i64 Timestamp

struct User {
    1: i32 id,
    2: string email,
    3: string username
}

enum RoomType {
    PRIVATE = 0,
    PUBLIC = 1
}

struct Room {
    1: i32 id,
    2: string name,
    3: RoomType type
}

struct Message {
    1: i32 id,
    2: User user,
    3: Room room,
    4: Timestamp timestamp,
    5: string msg
}
