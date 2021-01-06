#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h> 
#include <unistd.h>
#include <time.h>

const char* http_answer = "HTTP/1.1 200 OK\r\nContent-Length: 4\r\nContent-Type: text/plain\r\n\r\nGOOD";

char buf[4096];

void die(const char* msg) {
    fputs(msg, stderr);
    exit(1);
}

void run_worker(int sockfd);

int main() {
    int sockfd = socket(PF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        die("cannot create socket");
    }
    
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(80);

    if (bind(sockfd, (void*)&serv_addr, sizeof(serv_addr)) < 0) {
        die("cannot bind socket");
    }

    if (listen(sockfd, -1) < 0) {
        die("cannot listen socket");
    }

    char* WORKER_COUNT = getenv("WORKER_COUNT");
    int worker_count = WORKER_COUNT ? atoi(WORKER_COUNT) : 2;
    pid_t pid_list[worker_count];

    for (int i = 0; i < worker_count; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            run_worker(sockfd);
            exit(0);
        }

        pid_list[i] = pid;
    }

    sleep(3600);

    for (int i = 0; i < worker_count; i++) {
        waitpid(pid_list[i], NULL, 0);
    }
}

void run_worker(int sockfd) {
    pid_t pid = getpid();
    struct timespec delay = {0, 100 * 1000 * 1000};

    while (1) {
        int clientfd = accept(sockfd, NULL, 0);
        if (clientfd < 0) {
            printf("cannot accept: %d", -clientfd);
            continue;
        }

        read(clientfd, &buf, sizeof(buf));
        nanosleep(&delay, NULL);

        write(clientfd, http_answer, strlen(http_answer));
        close(clientfd);
    }
}
