{-# LANGUAGE OverloadedStrings #-}

module Main where

import qualified Chatroom_Types
import qualified Chatroom_2_Types

import Thrift
import Thrift.Protocol.Binary
import Thrift.Transport
import Thrift.Transport.Empty

import Data.ByteString.Lazy.Char8 (pack)
import Data.ByteString.Lazy.Internal (ByteString)
import Network
import System.Environment
import System.IO (hSetBuffering, hGetContents, BufferMode(..))


versionedDecode proto version contents = if (version == 1) then
            show $ Chatroom_Types.decode_Message proto contents
        else
            show $ Chatroom_2_Types.decode_Message proto contents


process version proto handle = do
    contents <- hGetContents handle

    print $ "Read: " ++ show contents

    print $ versionedDecode proto version $ pack contents


sockHandler version proto sock = do
    (handle, _, _) <- accept sock
    hSetBuffering handle NoBuffering
    print "Client connected"
    process version proto handle

    sockHandler version proto sock


serve version proto =  withSocketsDo $ do
    let port = 8003
    sock <- listenOn $ PortNumber port
    print $ "Listening on " ++ show port
    sockHandler version proto sock


main = do
    -- We explicitly set up a socket server to show just the data serialization

    --transport <- hOpen ("localhost", PortNumber 8003)

    args <- getArgs
    let version = if (length args > 0) && (args !! 0 == "v2") then 2 else 1

    print $ "Supported version: " ++ show version

    let transport = EmptyTransport
    let binProto = BinaryProtocol transport
    let client = (binProto, binProto)

    print "Hello"
    print $ show user
    print $ show $ Chatroom_Types.from_User user

    let encodedUser = Chatroom_Types.encode_User binProto user
    print $ show $ encodedUser

    serve version binProto


user = Chatroom_Types.User {
    Chatroom_Types.user_id = 1
  , Chatroom_Types.user_email = "xyz@localhost"
  , Chatroom_Types.user_username = "test-user"
}
