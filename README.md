# Data Exchange Formats

A showoff of data exchange formats. As a toy project, suppose we are making a chat room
with data structure as follows:

```
User:
    id:        Integer
    email:     String
    username:  String

Room:
    id:        Integer
    name:      String

Message:
    id:        Integer
    user:      User
    room:      Room
    timestamp: DateTime
    message:   String
```

