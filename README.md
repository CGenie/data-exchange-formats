# Data Exchange Formats

A showoff of data exchange formats. As a toy project, suppose we are making a chat room
with data structure as follows:

```
User:
    id:        Integer
    email:     String
    username:  String
    
RoomType:      Private | Public

Room:
    id:        Integer
    name:      String
    type:      RoomType

Message:
    id:        Integer
    user:      User
    room:      Room
    timestamp: DateTime
    message:   String
```

In version 2 of the protocol we extend the `User` model by adding the following fields:
```
    firstName: String
    lastName:  String
    age:       Integer
    badges:    String[]
```


# General remarks about data exchange formats

GitHub repo: https://github.com/CGenie/data-exchange-formats

Looking [philosophically](http://c2.com/cgi/wiki?DataAndCodeAreTheSameThing): data and code
are the same thing (see Lisp for example). Standard example of this is the definition [Church numerals](https://en.wikipedia.org/wiki/Church_encoding)
in Lambda calculus (we use Python here):
```
id = lambda x: x
zero = lambda f: id
one = lambda f: lambda x: f(x)
two = lambda f: lambda x: f(f(x))
three = lambda f: lambda x: f(f(f(x)))
```
Then this would mean that the multitude of data representations corresponds to the multitude of programming languages.

The ISO-standardized one is `ASN.1`. Big companies create and use their own:
- Protocol Buffers (Google)
- Thrift (Facebook)
- Bond (Microsoft)

Various schema-less formats also exist (samples encode `{'compact': True, 'schema': 0, 'name': 'Test'}`):
- [Concise Binary Object Representation (CBOR)](http://cbor.io/)
  ```
  00000000: a347 636f 6d70 6163 74f5 446e 616d 6544  .Gcompact.DnameD
  00000010: 5465 7374 4673 6368 656d 6100            TestFschema.
  ```
- [MessagePack](http://msgpack.org/)
  ```
  00000000: 83a7 636f 6d70 6163 74c3 a46e 616d 65a4  ..compact..name.
  00000010: 5465 7374 a673 6368 656d 6100            Test.schema.
  ```
  
Advantages of schema-based protocols is that the encoded message doesn't have to include the schema
which results in messages of smaller size and faster encoding/decoding (compare with `JSON` where
every serialized string also contains all schema info, object keys, etc). Also basic validation is for free.

JavaScript is special because it doesn't allow to run `FFI` code in browser. Thus, performance-wise, `JSON` is the
preferred format. That's why if you use something else, aim for schema-based ones for more type-safety and
other goodies. Here's the benchmark of `JSON` against `MessagePack`: https://jsperf.com/msgpack-js-vs-json

## Why not just stick with XML/JSON ?
([quote](https://ttsiodras.github.io/asn1.html)) "If you value optimal encoding/decoding performance, minimal encoded message size, guarantees of code safety, and minimal power requirements for encoding/decoding messages, then no, `XML` is most definitely NOT better. That's why your mobile phone has used `ASN.1` encoding while you were reading this article. I am not kidding - almost every single signalling message that your phone sends to the local cell tower, is encoded via `ASN.1`!
If on the other hand...
- you don't care for performance or safety requirements, and `XML` parsing is cheap in your problem domain
- you have lots of memory to waste and don't care about optimal message representations
- you want to easily peek into the encoded streams and figure out things during debugging (but read below for `XER`, and also note that [wireshark](https://www.wireshark.org/) has an `ASN.1` inspector)
- you have other development dependencies, like extensive use of `XPath`..."

Note that Wikipedia [defines `XML` as not human-readable!](http://en.wikipedia.org/wiki/Data_exchange): ![Alt text](./Data exchange - Wikipedia, the free encyclopedia 2015-06-14 08-31-54.png)

After your API is working -- how often do you need to read the serialized message? I think not very often and if so it's for debugging reasons. You care about _content_ and not specific format representation.

After initial development you can use the [content negotiation of `HTTP`](https://en.wikipedia.org/wiki/Content_negotiation) to use the binary format. You can expose the various formats by using [the `OPTIONS` method of `HTTP`](http://zacstewart.com/2012/04/14/http-options-method.html).


## Bond
Serialization system is written [partially in Haskell](http://blog.nullspace.io/bond-oss.html).
[Couple differences from other formats](https://microsoft.github.io/bond/why_bond.html)

## Performance comparison
From https://github.com/sidshetye/SerializersCompare (for C#):
```
1000 iterations per serializer, average times listed
Sorting result by size
Name                Bytes  Time (ms)
------------------------------------
Avro (cheating)       133     0.0142
Avro                  133     0.0568
Avro MSFT             141     0.0051
Thrift (cheating)     148     0.0069
Thrift                148     0.1470
ProtoBuf              155     0.0077
MessagePack           230     0.0296
ServiceStackJSV       258     0.0159
Json.NET BSON         286     0.0381
ServiceStackJson      290     0.0164
Json.NET              290     0.0333
XmlSerializer         571     0.1025
Binary Formatter      748     0.0344

Options: (T)est, (R)esults, s(O)rt order, (S)erializer output, (D)eserializer output (in JSON form), (E)xit

Serialized via ASN.1 DER encoding to 148 bytes in 0.0674ms (hacked experiment!)
```

From https://github.com/eishay/jvm-serializers (for Java):
```
                                   create     ser   deser   total   size  +dfl
                                   java-built-in                          63    5838   30208   36046    889   514
                                   hessian                                63    3881    6176   10057    501   313
                                   kryo                                   63     655     838    1493    212   132
                                   fast-serialization                     63     704     864    1568    252   166
                                   jboss-serialization                    63    6466    6643   13110    932   582
                                   jboss-marshalling-river                63    4656   23892   28548    694   400
                                   protostuff                             82     495     732    1227    239   150
                                   msgpack-databind                       62     830    1370    2200    233   146
                                   json/jackson/databind                  62    1895    2600    4496    485   261
                                   json/jackson/db-afterburner            63    1513    1988    3501    485   261
                                   json/protostuff-runtime                63    1532    2138    3670    469   243
                                   json/google-gson/databind              63    5633    4844   10477    486   259
                                   json/svenson-databind                  63    5270   10358   15628    495   272
                                   json/flexjson/databind                 63   19445   25394   44838    503   273
                                   json/fastjson/databind                 63    1316    1149    2465    486   262
                                   smile/jackson/databind                 63    1768    1891    3659    338   241
                                   smile/jackson/db-afterburner           64    1448    1492    2940    352   252
                                   bson/jackson/databind                  64    5376    6812   12188    506   286
                                   xml/xstream+c                          64    6476   13505   19981    487   244
                                   xml/jackson/databind-aalto             63    3001    5516    8517    683   286
                                   ```



