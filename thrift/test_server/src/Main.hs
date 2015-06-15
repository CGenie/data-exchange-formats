{-# LANGUAGE OverloadedStrings #-}

module Main where

import Chatroom_Types

import Thrift
import Thrift.Protocol.Binary
import Thrift.Transport
import Thrift.Transport.Empty

import Data.ByteString.Lazy.Char8 (pack)
import Network
import System.IO (hSetBuffering, hGetContents, BufferMode(..))


process proto handle = do
    contents <- hGetContents handle

    print $ "Read: " ++ show contents

    let message = decode_Message proto $ pack contents

    print $ show message


sockHandler proto sock = do
    (handle, _, _) <- accept sock
    hSetBuffering handle NoBuffering
    print "Client connected"
    process proto handle

    sockHandler proto sock


serve proto =  withSocketsDo $ do
    let port = 8003
    sock <- listenOn $ PortNumber port
    print $ "Listening on " ++ show port
    sockHandler proto sock


main = do
    -- We explicitly set up a socket server to show just the data serialization

    --transport <- hOpen ("localhost", PortNumber 8003)

    let transport = EmptyTransport
    let binProto = BinaryProtocol transport
    let client = (binProto, binProto)

    print "Hello"
    print $ show user
    print $ show $ from_User user

    let encodedUser = encode_User binProto user
    print $ show $ encodedUser

    serve binProto


user = User {
    user_id = 1
  , user_email = "xyz@localhost"
  , user_username = "test-user"
}
