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

#include <FooQuestion.h>

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

    FooQuestion_t* question;
    asn_enc_rval_t ec;
    OCTET_STRING_t *q;
    const char QUESTION[] = "What's your name?";
    char *output = calloc(100, sizeof(char));

    question = calloc(1, sizeof(FooQuestion_t));

    question->trackingNumber = 5;
    q = OCTET_STRING_new_fromBuf(&asn_DEF_IA5String, QUESTION, strlen(QUESTION));

    question->question = *q;

    ec = der_encode(&asn_DEF_FooQuestion, question, write_string, output);

    asn_fprint(stdout, &asn_DEF_FooQuestion, question);
    //xer_fprint(stdout, &asn_DEF_FooQuestion, question);

    memset(recvBuff, '0',sizeof(recvBuff));

    send(sockfd, output, ec.encoded, 0);

    free(output);

    return 0;
}