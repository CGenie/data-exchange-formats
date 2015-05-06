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
