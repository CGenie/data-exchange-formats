#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

#include <Room.h>
#include <RoomType.h>
#include <Message.h>
#include <User.h>

#define HOSTNAME "127.0.0.1"
#define PORT 8001


int initialize_socket() {
    int sockfd;
    struct sockaddr_in serv_addr;

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Error : Could not create socket \n");
        exit(1);
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, HOSTNAME, &serv_addr.sin_addr) <= 0)
    {
        printf("\n inet_pton error occured\n");
        exit(1);
    }

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
       printf("\n Error : Connect Failed \n");
       exit(1);
    }

    return sockfd;
}


static int write_stream(const void *buffer, size_t size, void *app_key) {
    FILE *out_fp = app_key;
    size_t wrote;

    wrote = fwrite(buffer, 1, size, out_fp);

    return (wrote == size) ? 0 : -1;
}


// primitive stream implementation
int position = 0;


static int write_string(const void *buffer, size_t size, void *app_key) {
    char *output = app_key;
    size_t wrote = size;

    strncpy(output + position, buffer, size);

    position += size;

    return (wrote == size) ? 0 : -1;
}


int main(int argc, char* argv[]) {
    int sockfd = initialize_socket();
    int n = 0;
    char recvBuff[1024];
    int tmp;

    User_t* user;
    int user_id[] = {1, 1};
    const char EMAIL[] = "abx@localhost";
    const char USERNAME[] = "TestUser";

    RoomType_t* rt;

    Room_t* room;
    int room_id[] = {2, 1};
    const char ROOMNAME[] = "Test Room";

    Message_t* message;
    // NOTE: set message_id[] to {3, 1} and you get <absent> message_id ?
    // Code in OBJECT_IDENTIFIER.c reveals some special treatment for first
    // value being in 0..2 range. Strange!
    int message_id[] = {2, 2};
    const char MESSAGE[] = "This is a test message";

    asn_enc_rval_t ec;
    OCTET_STRING_t *q;
    char *output = calloc(1000, sizeof(char));

    // USER
    user = calloc(1, sizeof(User_t));
    // User.id (returning temporary variable)
    tmp = OBJECT_IDENTIFIER_set_arcs(&user->id, user_id, sizeof(user_id[0]), sizeof(user_id) / sizeof(user_id[0]));
    // User.email
    q = OCTET_STRING_new_fromBuf(&asn_DEF_UTF8String, EMAIL, strlen(EMAIL));
    user->email = *q;
    // User.username
    q = OCTET_STRING_new_fromBuf(&asn_DEF_UTF8String, USERNAME, strlen(USERNAME));
    user->username = *q;

    // ROOMTYPE
    rt = calloc(1, sizeof(RoomType_t));
    rt->present = RoomType_PR_public;

    // ROOM
    room = calloc(1, sizeof(Room_t));
    // Room.id
    tmp = OBJECT_IDENTIFIER_set_arcs(&room->id, room_id, sizeof(room_id[0]), sizeof(room_id) / sizeof(room_id[0]));
    // Room.name
    q = OCTET_STRING_new_fromBuf(&asn_DEF_UTF8String, ROOMNAME, strlen(ROOMNAME));
    room->name = *q;
    // Room.type
    room->type = *rt;

    // MESSAGE
    message = calloc(1, sizeof(Message_t));
    // Message.id
    // NOTE: Try to comment this line and see how server reacts
    tmp = OBJECT_IDENTIFIER_set_arcs(&message->id, message_id, sizeof(message_id[0]), sizeof(message_id) / sizeof(message_id[0]));
    // Message.user
    message->user = *user;
    // Message.room
    message->room = *room;
    // Message.message
    q = OCTET_STRING_new_fromBuf(&asn_DEF_UTF8String, MESSAGE, strlen(MESSAGE));
    message->message = *q;

    ec = der_encode(&asn_DEF_Message, message, write_string, output);

    asn_fprint(stdout, &asn_DEF_User, user);
    asn_fprint(stdout, &asn_DEF_RoomType, rt);
    asn_fprint(stdout, &asn_DEF_Room, room);
    asn_fprint(stdout, &asn_DEF_Message, message);
    //xer_fprint(stdout, &asn_DEF_User, user);

    memset(recvBuff, '0', sizeof(recvBuff));

    send(sockfd, output, ec.encoded, 0);

    free(output);

    return 0;
}
