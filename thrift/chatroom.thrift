/* Specification of a simple chatroom protocol */

ChatRoomProtocol DEFINITIONS ::= BEGIN

    User ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        email          UTF8String (SIZE(1..40)),
        username       UTF8String (SIZE(1..40)),
        ...
    }

    RoomType ::= CHOICE {
        private    [0] NULL,
        public     [1] NULL
    }

    Room ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        name           UTF8String (SIZE(1..40)),
        type           RoomType
    }

    Message ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        user           User,
        room           Room,
        message        UTF8String (SIZE(1..128))
    }

END
