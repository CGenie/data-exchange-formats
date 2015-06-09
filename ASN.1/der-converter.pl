#!/usr/bin/env perl

use Convert::ASN1;
use Data::Dumper;

$asn = Convert::ASN1->new ("encoding" => "DER");

#$file_contents = do {
#    local $/ = undef;
#    open $fh, "<", "chatroom.asn";
#    <$fh>
#};
#$asn->prepare($file_contents);

#$asn->prepare_file("chatroom.asn");

$asn->prepare(q<
    User ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        email          UTF8String, -- (SIZE(1..40)),
        username       UTF8String -- (SIZE(1..40))
    }

    RoomType ::= CHOICE {
        private    [0] NULL,
        public     [1] NULL
    }

    Room ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        name           UTF8String, -- (SIZE(1..40)),
        type           RoomType
    }

    Message ::= SEQUENCE {
        id             OBJECT IDENTIFIER,
        user           User,
        room           Room,
        message        UTF8String -- (SIZE(1..128))
    }
>) or die $asn->error;

#print Dumper($asn), "\n";

#$pdu = $asn->encode( int => 7, str => "string");

$der_contents = do {
    local $/ = undef;
    open $fh, "<", "server-message-received";
    <$fh>
};

print $der_contents, "\n";

$out = $asn->decode($der_contents) or die $asn->error;

print Dumper($out->tree->Message), "\n";
