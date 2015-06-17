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

# Some notes

[Thrift: The Missing Guide](http://diwakergupta.github.io/thrift-missing-guide/)

Apart from primitive types: `bool`, `byte`, `i16`, `i32`, `i64`, `double`, `string` also
container types are supported: `list<t1>`, `set<t1>`, `map<t1,t2>`. And you also have
`const`, `enum` and `struct`.

You can include other Thrift files with: `include "some-other-file.thrift"`.

Structs require an integer identifier, this is called 'tags' in other schemas.
