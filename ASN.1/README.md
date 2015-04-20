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
