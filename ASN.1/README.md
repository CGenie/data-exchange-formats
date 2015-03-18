Install Python packages from `requirements.txt`

Install git://github.com/vlm/asn1c.git:
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

Also please adjust paths in `generate-codec.sh` to point to your cloned `asn1c` repo.

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
./test-client
```
to test the C client.
