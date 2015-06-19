# Apache Thrift

## Building code
Run `make init` to build thrift definitions.

To build the server you need to clone the `apache-thrift` repo, because Haskell library is broken
(see [this thread](http://webmail.dev411.com/t/thrift/dev/152jpq1hpm/jira-created-thrift-3003-missing-license-file-prevents-package-from-being-installed))
```
git clone -b 0.9.2 https://github.com/apache/thrift.git thrift.git

cd test_server
cabal sandbox init
cabal sandbox add-source ../thrift.git/lib/hs
cabal install --dependencies-only
cabal build
```

Then run server with:
```
./dist/build/test-server/test-server
```

For the Ruby client:
```
gem install bundler
bundle install
```

## Some notes

[Thrift: The Missing Guide](http://diwakergupta.github.io/thrift-missing-guide/)

[Official language support](http://wiki.apache.org/thrift/LibraryFeatures?action=show&redirect=LanguageSupport):
- C++
- C#
- Erlang
- Haskell
- Java
- JavaScript
- Python
- Ruby
- and many others with different protocols/transport support

Thrift is [used by](http://wiki.apache.org/thrift/PoweredBy):
- [Facebook](http://www.facebook.com) https://code.facebook.com/posts/1468950976659943/under-the-hood-building-and-open-sourcing-fbthrift/
- [Hadoop](https://hadoop.apache.org/) http://wiki.apache.org/hadoop/Hbase/ThriftApi
- [Cassandra](http://cassandra.apache.org/) DID use to support Thrift but they
  [switched to CQL](http://planetcassandra.org/making-the-change-from-thrift-to-cql/)
- [Evernote](https://evernote.com/) http://blog.evernote.com/tech/2011/05/26/evernote-and-thrift/
- [LastFM](http://www.last.fm/)

Code generator is written in `C++`.

Apart from primitive types: `bool`, `byte`, `i16`, `i32`, `i64`, `double`, `string` also
container types are supported: `list<t1>`, `set<t1>`, `map<t1,t2>`. And you also have
`const`, `enum` and `struct`.

You can include other Thrift files with: `include "some-other-file.thrift"`.

Structs require an integer identifier, this is called 'tags' in other schemas.

Multiple serialization formats are supported: Haskell has `Binary`, `Compact` and `JSON`,
Java has additionally `multiplexed`, `simple JSON`, `tuple`.

Also various transports are provided out of the box: `Empty`, `Framed`, `HttpClient` for
Haskell for example.
