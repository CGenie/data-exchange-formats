# ASN.1 (Abstract Syntax Notation)

Some examples of [usages](http://www.marben-products.com/asn.1/market.html) [of ASN.1](http://www.itu.int/en/ITU-T/asn1/Pages/Application-fields-of-ASN-1.aspx):
- Universal Mobile Telecommunication System (UMTS)
- LTE -- uses ASN.1 for control messages
- Smart cards (SIM)
- Lighweight Directory Access Protocol (LDAP) -- [Complete Definition of the LDAP protocol in ASN.1](https://tools.ietf.org/html/rfc4511#appendix-B)
- Radio Frequency Identification (RFID)
- Aeronautical Telecommunication Network (ATN)
- Public-Key Cryptography Standards (PKCS)
- Internet X.509 Public Key Infrastructure (PKI)

## How to run the code
Install Python packages from `requirements.txt`

Install https://github.com/vlm/asn1c:
```
autoreconf -iv
./configure
make
make install
```
It might be required to add
```
m4_ifdef([AM_PROG_AR], [AM_PROG_AR])
```
to the `configure.ac` file if `autoreconf` fails.
I installed `asn1c` into `$HOME/asn1c-bin`, please adjust paths in `generate-codec.sh` to match your installation.

Then you can test ASN.1 in the following way:

```
./generate-codec.sh
```
to generate ASN.1 codecs for Python and C.

```
./test-server.py
```
to fire up the simple server.
```
./test-client.py
```
to test the Python client.
```
make
./test-client
```
to test the C client.


## Conclusions

With ASN.1 you are not bound to XML, JSON or whatever, with JSONSchema it's only JSON. And since ASN.1 is about data
and not it's format, you can [encode ASN.1 to JSON](http://www.obj-sys.com/docs/JSONEncodingRules.pdf).

In Python JSON serialization is much faster than ASN.1 but when you throw in `jsonschema` validation it becomes
much slower:

```
$ python perf-test.py

ASN1 time: 0.17259311676
JSON time: 0.00303816795349
JSON with schema validation time: 2.8563849926
```

Error messages when some ASN.1 fields are missing can be cryptic:

```
Traceback (most recent call last):
  File "perf-test.py", line 82, in <module>
    encoder.encode(m)
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/codec/der/encoder.py", line 26, in __call__
    return encoder.Encoder.__call__(self, client, defMode, maxChunkSize)
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/codec/cer/encoder.py", line 83, in __call__
    return encoder.Encoder.__call__(self, client, defMode, maxChunkSize)
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/codec/ber/encoder.py", line 348, in __call__
    self, value, defMode, maxChunkSize
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/codec/ber/encoder.py", line 52, in encode
    encodeFun, value, defMode, maxChunkSize
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/codec/ber/encoder.py", line 250, in encodeValue
    value.setDefaultComponents()
  File "/home/przemek/.virtualenvs/python27/lib/python2.7/site-packages/pyasn1/type/univ.py", line 818, in setDefaultComponents
    'Uninitialized component #%s at %r' % (idx, self)
pyasn1.error.PyAsn1Error: Uninitialized component #3 at Message().setComponentByPosition(0, ObjectIdentifier(3.1)).setComponentByPosition(1, User().setComponentByPosition(0, ObjectIdentifier(1.1)).setComponentByPosition(1, UTF8String('xyz@localhost')).setComponentByPosition(2, UTF8String('User'))).setComponentByPosition(2, Room().setComponentByPosition(0, ObjectIdentifier(2.1)).setComponentByPosition(1, UTF8String('Test Room')).setComponentByPosition(2, RoomType().setComponentByPosition(1, Null(''))))
```

ASN.1 supports a wide range of types, including things like [GeneralizedTime](http://www.obj-sys.com/asn1tutorial/node14.html)


# Notes about ASN.1

`ASN.1` is a schema language with multiple set of encoding rules, while `JSON` is a data format.

[`ASN.1` playground](http://asn1-playground.oss.com/)

[Encoding rules](http://www.oss.com/asn1/resources/asn1-made-simple/encoding-rules.html)

`OpenSSL` [includes](https://www.openssl.org/docs/apps/asn1parse.html) an `ASN.1` parser: `openssl asn1parse -in ~/.ssh/id_rsa.asn1-test` (_WARNING_: file needs to be unencrypted, if it is encrypted use `openssl rsa -in <encrypted_file> -out <unencrypted_file>`).

## Birth of ASN.1
In 1984 the Telegraph and Telephone Consultative Commitee (part of the International Telecommunication Union) standardized the
notation X.409 ("Message Handling Sytems: Presentation Transfer Syntax and Notation") developed by James White and
Douglas Steedman. It defined the built-in types of: `ANY`, `BIT STRING`, `BOOLEAN`, `CHOICE`, `INTEGER`, `NULL`,
`OCTET STRING`, `SEQUENCE`, `SEQUENCE OF`, `SET`, `SET OF` and the character string types: `IA5String`, `NumericString`,
`PrintableString`, `T61String`, `VideotexString`, `GeneralizedTime`, `UTCTime`. This standard was independent of
the Message Handling System and so other commitees started using it. They called it `ASN.1`, the ".1" implying in ISO way
that there could be more such formats, but to this day there does not exist `ASN.2`. `ASN.1` was standardized on its own
in 1987 under references ISO 8824 and ISO 8825. The ISO and ITU-T commitees have joined their forces in 1998.

## Random remarks
- The specification breaks down into one or several modules.
- The specifier can restrict which definitions it exports with the `EXPORTS` clause (without `EXPORTS` all definitions are exported).
- The generality of `INTEGER` is sometimes held against `ASN.1` but the specifier can just add range definition and for example for range
  `INTEGER (12345..12346)` the `PER` encoder would encode this number on a single bit.
- There are many different exotic string types, which is a legacy of old technologies like Videotex (Minitel for example)
  [!Minitel](http://cdn.arstechnica.net//wp-content/uploads/2012/06/4271111360_dc27809b59_o.jpg)
- Not only `INTEGER` ranges are allowed as in `INTEGER (1..40)` but also character ranges as in
  ```
  upperCase UTF8String (FROM("A".."Z"))
  ```
  Unfortunately, it seems that `pyasn1` doesn't support this.
- Universal, uniquely-defined datatypes can be created by using the `OBJECT IDENTIFIER` clause.
- The `ASN.1` bug: https://jbp.io/2015/06/11/cve-2015-1788-openssl-binpoly-hang/
- ASN.1, protobuf - self-documenting, with JSON you need: return JSON, validate fields, document fields - that's 3 times rewriting code
- Don't know how to define `DEFAULT` subtype of type, i.e.:

```
RoomType ::= CHOICE {
    private [0] NULL,
    public [1] NULL
}

Room ::= SEQUENCE {
    type RoomType DEFAULT ???
}
```
- Lots  of types to choose from, in particular `SET`,  `BIT STRING`,`NumericString` (sometimes types are with only uppercase letters, sometimes they are in CamelCase, this is for historical reasons).

- Can include value-reference-names:

```
my-variable INTEGER ::= 20

some-field INTEGER DEFAULT my-variable
```

- Can have enumerable ints:

```
choices INTEGER {
    one (1),
    two (2),
    three (3)
} DEFAULT one
```
or
```
choices ::= ENUMERATED {
   one,
   two,
   three
}
```

-`REAL` type has curious notation:
```
v1 REAL ::= { mantissa 1, base 10, exponent -5 }
``` 
but you have the pre-defined values `PLUS-INFINITY` and `MINUS-INFINITY`.

- `ASN.1` supports macros though it's a controversial feature.

- Parametrization of types:
```
My-Type {INTEGER : dummy1, Dummy2} ::= SEQUENCE {
    first-field Dummy2,
    second-field INTEGER (1.dummy1)
}
```
Then you use it like:
```
my-field ::= My-Type{1, UTF8String}
```
Unfortunately, it seems that `pyasn1` doesn't support parametrization of types.

- `ASN.1` allows strings to match some Regexp pattern as in:
```
dateAndTime ::= VisibleString (PATTERN "\d#2/\d#2/\d#4-\d#2:\d#2") -- DD/MM/YYYY-HH:MM
```
Unfortunately, it seems that `pyasn1` doesn't support this.

- You can encode `ASN.1` in your favorite `JSON` format: http://www.obj-sys.com/docs/JSONEncodingRules.pdf 
- Redditors opinions about `ASN.1` are very extreme: http://www.reddit.com/r/programming/comments/1hf7ds/useful_old_technologies_asn1/ (provide some quotes)
- Some quotes from [Eric Naggum's](http://en.wikipedia.org/wiki/Erik_Naggum) post regarding `ASN.1`:
  - "This experiment was among the many data points that led me to conclude that SGML is insane and that those who think it is rational to require parsing of character data at each and every application interface are literally retarded and willfully blind.  Also, an SDIF data stream can only represent a validated document and the kinds of errors you get when parsing ASN.1 are unforgiving."
  -  "But, alas, people prefer buggy text formats that they can approximate rather than precise binary formats that follow general rules that are make them as easy to use as text formats."
  -  JavaScript supports seems to be quite bad:
    - https://www.npmjs.com/package/asn1 only supports `BER`, not maintained for some time now
    - http://kjur.github.io/jsrsasign/ is a cryptographic library with some `ASN.1` support
    - Some online viewers exist: http://www.geocities.co.jp/SiliconValley-SanJose/3377/asn1JS.html, http://lapo.it/asn1js/ but they do not convert to some native JavaScript datatypes
    - https://github.com/GlobalSign/ASN1.js seems to be quite OK (only `BER` seems to be supported) but lacks a string parser of schemas (you must construct it using JavaScript objects)
 - ["The one big thing about ASN.1 is, that ist is designed for specification not implementation. Therefore it is very good at hiding/ignoring implementation detail in any "real" programing language."](http://stackoverflow.com/a/13221519)
 - [A very good explanation of `IMPLICIT` and `EXPLICIT`](http://www.mail-archive.com/asn1@oss.com/msg01062.html)
 - Supports `IMPORTS` and `EXPORTS` clauses for module imports/exports ([see here](http://www.cse.msu.edu/rgroups/sens/Software/Telelogic-3.5/locale/english/help/htmlhlp/asn1util.html)).

## Extensibility of ASN.1

[Notes about extensibility of ASN.1](http://lionet.info/asn1c/blog/2010/09/21/question-extensibility-removing-fields/)

You can either use `...` after all non-extensible fields are present or use `EXTENSIBILITY IMPLIED` module option.


## GSER Encoding
Human-readable. From [Wikipedia](https://en.wikipedia.org/wiki/Generic_String_Encoding_Rules):
"Generic String Encoding Rules (GSER) are a set of ASN.1 encoding rules for producing a verbose, human-readable textual transfer syntax for data structures described in ASN.1.

The purpose of GSER is to represent encoded data to the user or input data from the user, in a very straightforward format. GSER was originally designed for the Lightweight Directory Access Protocol (LDAP) and is rarely used outside of it. The use of GSER in actual protocols is discouraged since not all character string encodings supported by ASN.1 can be reproduced in it.

The GSER encoding rules are specified in RFC 3641 and unlike other common types of encoding rules, are not standardised by ITU-T."

## BER Encoding
Has lots of way to encode.

Each type has a tag:

| Type | Tag number (decimal) | Tag number (hexadecimal) |
|:----:|:--------------------:|:------------------------:|
| `INTEGER` | 2 | 02 |
| `BIT STRING` | 3 | 03 |
| `OCTET STRING` | 4 | 04 |
| `NULL` | 5 | 05 |
| `OBJECT IDENTIFIER` | 6 | 06 |
| `SEQUENCE and SEQUENCE OF` | 6 | 10 |
| `SET and SET OF` | 17 | 11 |
| `PrintableString` | 19 | 13 |
| `T61String` | 20 | 14 |
| `IA5String` | 22 | 16 |
| `UTCTime` | 23 | 17 |

`BER` Encoding has four parts:

- _Identifier octets_: These identify the class and tag number of the ASN.1 value, and indicate whether the method is primitive or constructed.
- _Length octets_: For the definite-length methods, these give the number of contents octets. For the constructed, indefinite-length method, these indicate that the length is indefinite.
- _Contents octets_: For the primitive, definite-length method, these give a concrete representation of the value. For the constructed methods, these give the concatenation of the BER encodings of the components of the value.
- _End-of-contents octets_: For the constructed, indefinite- length method, these denote the end of the contents. For the other methods, these are absent. 

From Wikipedia: "The key difference between the BER format and the CER or DER formats is the flexibility provided by the Basic Encoding Rules. BER, as explained above, is the basic set of encoding rules given by ITU X.690 for the transfer of ASN.1 data structures. It gives senders clear rules for encoding data structures they want to send, but also leaves senders some encoding choices. As stated in the X.690 standard, "Alternative encodings are permitted by the basic encoding rules as a sender's option. Receivers who claim conformance to the basic encoding rules shall support all alternatives".[1]

A receiver must be prepared to accept all legal encodings in order to legitimately claim BER-compliance. By contrast, both CER and DER restrict the available length specifications to a single option. As such, CER and DER are restricted forms of BER and serve to disambiguate the BER standard."

## DER Encoding

`DER`-encoded string can be `BER`-decoded but not vice versa (`BER`-encoded string cannot in general be decoded with `DER`).

DER encoding of message:

```
Message:
 id=2.2
 user=User:
  id=1.1
  email=abx@localhost
  username=TestUser

 room=Room:
  id=2.1
  name=Test Room
  type=RoomType:
   public=


 message=This is a test message
```

produces:

```
00000000: 304d 0601 5230 1c06 0129 0c0d 6162 7840  0M..R0...)..abx@
00000010: 6c6f 6361 6c68 6f73 740c 0854 6573 7455  localhost..TestU
00000020: 7365 7230 1206 0151 0c09 5465 7374 2052  ser0...Q..Test R
00000030: 6f6f 6da1 0205 000c 1654 6869 7320 6973  oom......This is
00000040: 2061 2074 6573 7420 6d65 7373 6167 65     a test message
```

(use `xxd server-message-received` in `ASN.1` source code).

[The above message in JavaScript `ASN.1` decoder](https://lapo.it/asn1js/#304D060152301C0601290C0D616278406C6F63616C686F73740C08546573745573657230120601510C095465737420526F6F6DA10205000C165468697320697320612074657374206D657373616765).

[Some info on how `OBJECT IDENTIFIER` is encoded in `DER`](https://msdn.microsoft.com/en-us/library/bb540809%28v=vs.85%29.aspx).

Also check this out: `openssl asn1parse -inform DER -in server-message-received`
```
    0:d=0  hl=2 l=  77 cons: SEQUENCE          
    2:d=1  hl=2 l=   1 prim: OBJECT            :2.2
    5:d=1  hl=2 l=  28 cons: SEQUENCE          
    7:d=2  hl=2 l=   1 prim: OBJECT            :1.1
   10:d=2  hl=2 l=  13 prim: UTF8STRING        :abx@localhost
   25:d=2  hl=2 l=   8 prim: UTF8STRING        :TestUser
   35:d=1  hl=2 l=  18 cons: SEQUENCE          
   37:d=2  hl=2 l=   1 prim: OBJECT            :2.1
   40:d=2  hl=2 l=   9 prim: UTF8STRING        :Test Room
   51:d=2  hl=2 l=   2 cons: cont [ 1 ]        
   53:d=3  hl=2 l=   0 prim: NULL              
   55:d=1  hl=2 l=  22 prim: UTF8STRING        :This is a test message
```

`DER` encoding is used to encode `PEM` files (from [here](https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem)):

"In essence `PEM` files are just base64 encoded versions of the `DER` encoded data. In order to distinguish from the outside what kind of data is inside the `DER` encoded string, a header and footer are present around the data. An example of a `PEM` encoded file is:

```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDMYfnvWtC8Id5bPKae5yXSxQTt
+Zpul6AnnZWfI2TtIarvjHBFUtXRo96y7hoL4VWOPKGCsRqMFDkrbeUjRrx8iL91
4/srnyf6sh9c8Zk04xEOpK1ypvBz+Ks4uZObtjnnitf0NBGdjMKxveTq+VE7BWUI
yQjtQ8mbDOsiLLvh7wIDAQAB
-----END PUBLIC KEY-----
```

(`BEGIN PUBLIC KEY` and `END PUBLIC KEY` are indicators that inside `DER` encoding is used).

The above [decodes](https://lapo.it/asn1js/#30819F300D06092A864886F70D010101050003818D0030818902818100CC61F9EF5AD0BC21DE5B3CA69EE725D2C504EDF99A6E97A0279D959F2364ED21AAEF8C704552D5D1A3DEB2EE1A0BE1558E3CA182B11A8C14392B6DE52346BC7C88BF75E3FB2B9F27FAB21F5CF19934E3110EA4AD72A6F073F8AB38B9939BB639E78AD7F434119D8CC2B1BDE4EAF9513B056508C908ED43C99B0CEB222CBBE1EF0203010001) to:
```
SEQUENCE(2 elem)
  SEQUENCE(2 elem)
    OBJECT IDENTIFIER 1.2.840.113549.1.1.1
    NULL
  BIT STRING(1 elem)
    SEQUENCE(2 elem)
    INTEGER(1024 bit) 143522426776494817924661546336042357659457754309782820456976070197510…
    INTEGER 65537
```

the `ASN.1` schema being:
```
RSAPublicKey ::= SEQUENCE {
    modulus           INTEGER,  -- n
    publicExponent    INTEGER   -- e
}

PublicKeyInfo ::= SEQUENCE {
  algorithm       AlgorithmIdentifier,
  PublicKey       BIT STRING
}

AlgorithmIdentifier ::= SEQUENCE {
  algorithm       OBJECT IDENTIFIER,
  parameters      ANY DEFINED BY algorithm OPTIONAL
}
```

Private `RSA` key [decoded](https://lapo.it/asn1js/#308204A50201000282010100D8B5B389B296C471AA193FD7F5C025A01650FC941D6F95AEC320FF08E74601C1A4D74CFB8DADBB8AE1F15F18BE8C902BE6B4A96F525B3E687E2108F5A9716CEE24953B6FB6DAF7C9A16C224C45FF19CF8392D5254C03F0A96D05833ED993AD98C3D9BE53BF4439272E5281343FB81F27FCBEE7A3EACBA94EB51EEA52A50BE75BEF20A9D15937C1702BB9F46E3A95012B58591750516B97B295A42A8AC21BFD1862332BC46BD7ADD7092FD7A5ABECA85FE45B9AADA8198FEC19FBF9D0092F3D39CED0442C018DE3963913BCF4EED1DF978BD84779B0EA6C03C210360534939A2CF5AF9219DB0D7DC1971D8A2A6803D6BE28D67502D6F2DF8E064D0011B40F6D5702030100010282010100AC9E578BA878D5B3A0858A4850D5A462D743DD5D71F10F2EECF95C8CD00400A429D4E1DA42698FC8B9DF151BD5B48BA69C976D9B61E3925B939466D9A005DC79F923F1FB339149ED0F2ADE4B193A7169CD696964D31F145530A5427D0EBCC67BB80DBAC064CB4827408BB1A557D826E1283F3CAE61F9A63C2EA3988D0A30E830E83BDC02BB398B7FFE1E7A6ED62D7CDBA18EA87B67610AB563A60FEE13A82E967C1E94A06C03F44C83A9D706F3D9C84C792F4ED6413E127CDB5C338FA63B81393A2469EE188438ECB2EC451FDF4D513D972FCE48905C329AF89D97B251232DB75CE88C8CC4408E29FA99AE585E808EBDB1E8E2FDD353DC4C2FC1C9BF11DAD33102818100F5F757BCC74F5F62A3509B2547781F9069F7F45921CECA5A18856308C02676352811AE735AB814135B9FC959B423B27DB648C44FD6E709C27E05F10234A3936A232C95893F39010E795A8D924A9E04C0D8DD2E4A2B3A27863BEC9F6C6EE92B127F716268C94665A2030B065039EB8E0B72DBE65A8ADAAC0B156223605C48A5CF02818100E18CD47CDC591C6F1A7689A2DD7C215389A5767FB50E5F3382E797B05C951E89D832EF1E088DEEC44F8EB7F58964D4CCE27D86F8132C5B331457AFD167FF0A730D9159D5A01B00690A8EBB44F0EC74B0B10AB710E1195963DB1003E05ED02A6305B67A3E9F57C5DDF847EC8E4EA1FFFB38DCA24A0D495869D166650351A829F90281801FA6592AD876B52E6B17672F4FD7FC2FC802F8F5332D79CA481779DBD965D9961376DAFCCAF29EDAB2D287C53C31CFB8EF68C3A206642A5455850C331D74E2F6285A874F66CC3DFF8FCC00258FE66F742533A8CE306BC6443697C717DBD9B30A294DFCBCC11186E866FDD72D2196D6EB50374D97DF002E5D2ABE3B111E2ED6EF02818100C5C42E2CAD28957DF5BE2A40DBE393752424291B212E50DB61D49F74CC391465D9640FB64DD9E599CC085FD4B37BEDFB183CE8B36C5C603B1183316E73B974F81CD56DE79A5312B107C8CEFB4C2488CCC4EF9844FC9AB57E90FE21E8023A946FEEFA6985AF41CF052A46266D41155AD674AD40BF9D96CA273EAC81B5BF4BAC41028181009F5DC75E0BAF134F901E7F333020F69573745D62AF64EF932D335272C451B4B96445EB14A5DF252AC25E5A35D1023A9494BD61F6F0E4178B239CFCC77DEE4F5BBAA8E71CC7AD2620E9038B5648055E3BFCBA5412E4A116A869624D0419515E777C3E1E4D32C92A0CDC85CDF808CD91EDD741EB59380203FC36F3BA702EF2BC4C) (`~/.ssh/id_rsa.asn1-test`).

## PER Encoding

From Wikipedia: "Packed encoding rules (PER) are ASN.1 encoding rules for producing a compact transfer syntax for data structures described in ASN.1, defined in 1994.

This Recommendation or International Standard describes a set of encoding rules that can be applied to values of all ASN.1 types to achieve a much more compact representation than that achieved by the BER and its derivatives (described in ITU-T Rec. X.690 | ISO/IEC 8825-1).

It uses additional information, such as the lower and upper limits for numeric values, from the ASN.1 specification to represent the data units using the minimum number of bits. The compactness requires that the decoder knows the complete abstract syntax of the data structure to be decoded, however.

There are two variations of packed encoding rules: unaligned and aligned. With the unaligned encoding, the bits are packed with no regard for octet (byte) boundaries. With aligned encoding, certain types of data structures are aligned on octet boundaries, meaning there may be some number of wasted padding bits. Unaligned encoding uses the least number of bits, but presumably at some cost in processing time.

The packed encoding rules also define a restricted set of encoding rules, called CANONICAL-PER, which is intended to produce only a single possible encoding for any given data structure. CANONICAL-PER's role is therefore similar to the role of DER or CER."

From (http://www.w3.org/Protocols/HTTP-NG/asn1.html):
```
The packed encoding rules use a different style of encoding [from DER]. Instead of using a generic style of encoding that encodes all types in a uniform way, the PER specialise the encoding based on the data type to generate much more compact representations.

PER only generates tags when they are needed to prevent ambiguity this only occurs when ASN.1's version of union is used (CHOICE). PER also only generates lengths when the size of an object can vary. Even then, PER tries to represent the lengths in the most compact form possible.

PER encodings are not always aligned on byte boundaries- if the 'aligned' variant of the rules is used, then strings *will* be aligned - otherwise the encoding is treated as a string of bits, allowing things like booleans and small integers to be squished together in one byte.

The presence of optional elements in a sequence is indicated by a list of single bit flags placed at the start of a sequence - if the bit is set, then the option is present. 
```

## XER Encoding

From Wikipedia: "XML Encoding Rules (XER), defined in ITU-T standard X.693, are a set of ASN.1 encoding rules for producing an XML-based verbose textual transfer syntax for data structures described in ASN.1.

XER allows some flexibility with respect to, for example, white-space characters between XML elements. A variant of XER called Canonical XML Encoding Rules (CXER) is also defined for uses where encodings have to be deterministic, such as security exchanges. Data encoded in CXER is always valid XER, but not vice versa."

