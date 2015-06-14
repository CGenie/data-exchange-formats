Install Python packages from `requirements.txt`

Install NodeJS packages with `npm install`.

Start NodeJS server with `node test-server.js`.

Use the Python client with `python test-client.py`.

# Notes about Google's Protocol Buffers

- ["Why didn't you just use ASN.1?" The answer was "We never heard of it before."](http://www.reddit.com/r/programming/comments/1hf7ds/useful_old_technologies_asn1/cau70wc)
- [5 reasons why to use Protocol Buffers](http://blog.codeclimate.com/blog/2014/06/05/choose-protocol-buffers/) and in fact these are valid for `ASN.1` too:
  - schemas are present in `ASN.1` obviously
  - backward compatibility [is possible](https://www.evernote.com/shard/s120/view/8c26ac86-e821-4eec-a1c4-4eb994d6e60b?csrfBusterToken=U%3Dca4fc4%3AP%3D%2F%3AE%3D14db8148d09%3AS%3De0181a6d556dcc12ecc5cc786f11ce0d#st=p&n=8c26ac86-e821-4eec-a1c4-4eb994d6e60b)
  - less boilerplate (no encoding/decoding and validation)
  - validations and extensibility (?)
  - easy language interoperability -- true
- Whoa: `int32`, `int64`, `uint32`, `uint64`, `sint32`, `sint64`, `fixed32`, `fixed64`, `sfixed32`, `sfixed64`
- Some rules when defining `.proto` files (see also [this](https://developers.google.com/protocol-buffers/docs/proto#updating)):
   - you must not change the tag numbers of any existing fields.
   - you must not add or delete any required fields.
   - you may delete optional or repeated fields.
   - you may add new optional or repeated fields but you must use fresh tag numbers (i.e. tag numbers that were never used in this protocol buffer, not even by deleted fields).
   - Only one [official way](https://developers.google.com/protocol-buffers/docs/encoding) to encode/decode the structure
- Ecosystem seems to be quite well established:
  - JavaScript: https://github.com/dcodeIO/ProtoBuf.js/
    - It is way slower than traditional `JSON` encode/decode (because of no native support probably): http://jsperf.com/json-vs-protobuf
  - Clojure: https://github.com/flatland/clojure-protobuf
- `ASN.1` with `PER` encoding can be more compact: http://stackoverflow.com/a/4441622
- Based on `protobuf` Google released an RPC framework called [`gRPC`](http://www.grpc.io/).
