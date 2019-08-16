#include <openssl/sha.h>
#include <stdio.h>
#include <fcntl.h>

#define SZ 256

int main(int argc, char *argv[])
{
    int fd;
    char buff[SZ];
    int i = 0;

    SHA_CTX sha_ctx;
    unsigned char sha_hash[SHA_DIGEST_LENGTH];

    SHA1_Init(&sha_ctx);

    fd = open(argv[1], O_RDONLY, 0);

    do {

        i = read(fd, buff, SZ);

        SHA_Update(&sha_ctx, buff, i);

    } while (i>0);

    close(fd);

    SHA_Final(sha_hash, &sha_ctx);

    printf("\n\n Hash: ");
    for (i=0; i<SHA_DIGEST_LENGTH; i++) {
        printf("%x", sha_hash[i]);
    }
    printf("\n\n");
    return 0;
}
