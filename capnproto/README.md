# Cap'n Proto

This is a serialization system as well as an RPC framework.

## Schema language
[Source](https://capnproto.org/language.html)
- You cannot change a field, method, or enumerant’s number.
- You cannot change a field or method parameter’s type or default value.
- You cannot change a type’s ID.
- You cannot change the name of a type that doesn’t have an explicit ID, as the implicit ID is generated based in part on the type name.
- You cannot move a type to a different scope or file unless it has an explicit ID, as the implicit ID is based in part on the scope’s ID.
- You cannot move an existing field into or out of an existing union, nor can you form a new union containing more than one existing field

## RPC
Cap'n Proto's RPC system implements time travel: ![enter image description here](https://capnproto.org/images/time-travel.png)

From [the official docs](https://capnproto.org/rpc.html): "Cap’n Proto’s RPC protocol is based heavily on [CapTP](http://www.erights.org/elib/distrib/captp/index.html), the distributed capability protocol used by the [E programming language](http://www.erights.org/index.html). Lots of useful material for understanding capabilities can be found at those links."

### E programming language
http://www.erights.org/index.html

Recommended reading: [15 Minute Intro to E](http://www.erights.org/elang/intro/quickE.html)

