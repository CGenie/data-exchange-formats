init:
	thrift --gen rb chatroom.thrift
	thrift --gen rb chatroom_2.thrift

	thrift --gen hs chatroom.thrift
	thrift --gen hs chatroom_2.thrift

	cp gen-hs/*.hs test_server/src/
