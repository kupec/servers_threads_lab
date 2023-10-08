#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/types.h>
#include <sys/wait.h> 
#include <unistd.h>
#include <time.h>

const int SEC_TO_NSEC = 1000 * 1000 * 1000;
const int MSEC_TO_NSEC = 1000 * 1000;
const int DELAY = 100 * MSEC_TO_NSEC;

const char* http_answer = "HTTP/1.1 200 OK\r\nContent-Length: 4\r\nContent-Type: text/plain\r\n\r\nGOOD";

char buf[4096];

struct client_t {
    int fd;
    int wait_read;
    int wait_write;
    int wait_delay;
    struct timespec expire_at;
};

struct client_list_t {
    struct client_t array[FD_SETSIZE];
    int size;
};

struct client_list_t clients;

void die(const char* msg) {
    perror(msg);
    exit(1);
}

void log_client(const struct client_t *client, const char *line) {
    int index = client - &clients.array[0];
    printf("#%d: %s (fd=%d)\n", index, line, client->fd);
}

struct client_t *new_client() {
    struct client_t *result;
    for (int i = 0; i < clients.size; i++) {
         struct client_t *client = &clients.array[i];
         if (client->fd == 0) {
             return client;
         }
    }

    if (clients.size >= sizeof(clients.array)) {
        return NULL;
    }

    return &clients.array[clients.size++];
}

void accept_client(int sockfd) {
    //printf("Accepting socket\n");
    int fd = accept(sockfd, NULL, 0);
    if (fd < 0) {
        perror("accept()");
        return;
    }

    struct client_t *client = new_client();
    if (!client) {
        printf("Shutdown socket\n");
        shutdown(fd, SHUT_RDWR);
        return;
    }

    client->fd = fd;
    client->wait_read = 1;
    client->wait_write = 0;
    client->wait_delay = 0;
    client->expire_at.tv_sec = 0;
    client->expire_at.tv_nsec = 0;
    //log_client(client, "Accepted socket");
}

void close_client(struct client_t *client) {
    //log_client(client, "Closing socket");
    close(client->fd);
    client->fd = 0;
    client->expire_at.tv_sec = 0;
    client->expire_at.tv_nsec = 0;
}

void handle_client_read(struct client_t *client, struct timespec *now) {
    //log_client(client, "Reading socket");
    int count = read(client->fd, &buf, sizeof(buf));
    if (count < 0) {
        close_client(client);
        return;
    }

    client->expire_at = *now;

    client->expire_at.tv_nsec += DELAY;
    if (client->expire_at.tv_nsec > SEC_TO_NSEC) {
        client->expire_at.tv_nsec %= SEC_TO_NSEC;
        client->expire_at.tv_sec++;
    }
    client->wait_delay = 1;
    client->wait_read = 0;
}

void handle_client_delay(struct client_t *client, struct timespec *now) {
    //log_client(client, "Delaying socket");
    if (
        (now->tv_sec > client->expire_at.tv_sec) ||
        ((now->tv_sec == client->expire_at.tv_sec) && (now->tv_nsec > client->expire_at.tv_nsec))
    ) {
        //log_client(client, "Timeout");
        client->wait_write = 1;
        client->wait_delay = 0;
    }
}

void handle_client_write(struct client_t *client) {
    //log_client(client, "Writing to socket");
    client->wait_write = 0;
    write(client->fd, http_answer, strlen(http_answer));
    close_client(client);
}

void handle_timers(struct timespec *now) {
    for (int i = 0; i < clients.size; i++) {
        struct client_t *client = &clients.array[i];
        if (client->wait_delay) {
            handle_client_delay(client, now);
        }
    }
}

struct timeval get_time_delta(struct timespec from, struct timespec to) {
    struct timeval result = {0, 0};
    if (to.tv_sec < from.tv_sec) {
        return result;
    }
    if ((to.tv_sec == from.tv_sec) && (to.tv_nsec < from.tv_nsec)) {
        return result;
    }

    result.tv_sec = to.tv_sec - from.tv_sec;
    result.tv_usec = (to.tv_nsec - from.tv_nsec) / 1000;
    if (result.tv_usec < 0) {
        result.tv_usec += 1000 * 1000;
        result.tv_sec--;
    }

    return result;
}

int is_timeval_less(struct timeval a, struct timeval b) {
    if (a.tv_sec < b.tv_sec) {
        return 1;
    }
    if ((a.tv_sec == b.tv_sec) && (a.tv_usec < b.tv_usec)) {
        return 1;
    }
    return 0;
}

int main() {
    int sockfd = socket(PF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        die("cannot create socket");
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int)) < 0) {
        die("setsockopt");
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, &(int){1}, sizeof(int)) < 0) {
        die("setsockopt");
    }
    
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(8070);

    if (bind(sockfd, (void*)&serv_addr, sizeof(serv_addr)) < 0) {
        die("cannot bind socket");
    }

    if (listen(sockfd, -1) < 0) {
        die("cannot listen socket");
    }

    while (1) {
        fd_set rfds;
        fd_set wfds;
        struct timeval timeout;
        struct timespec now;
        timeout.tv_sec = 10;
        timeout.tv_usec = 0;
        if (clock_gettime(CLOCK_MONOTONIC, &now) < 0) {
            perror("clock_gettime");
            continue;
        }


        FD_ZERO(&rfds);
        FD_ZERO(&wfds);
        for (int i = 0; i < clients.size; i++) {
            struct client_t *client = &clients.array[i];
            if (client->wait_read) {
                FD_SET(client->fd, &rfds);
            }
            if (client->wait_write) {
                FD_SET(client->fd, &wfds);
            }

            if (client->expire_at.tv_sec && client->expire_at.tv_nsec) {
                struct timeval wait_time = get_time_delta(now, client->expire_at);
                if (is_timeval_less(wait_time, timeout)) {
                    timeout = wait_time;
                }
            }
        }
        FD_SET(sockfd, &rfds);

        int result = select(FD_SETSIZE, &rfds, &wfds, NULL, &timeout);
        if (result < 0) {
            perror("select()");
            exit(1);
        }

        if (clock_gettime(CLOCK_MONOTONIC, &now) < 0) {
            perror("clock_gettime");
            continue;
        }

        if (result == 0) {
            handle_timers(&now);
            continue;
        }

        for (int i = 0; i < clients.size; i++) {
            struct client_t *client = &clients.array[i];
            if (FD_ISSET(client->fd, &rfds)) {
                handle_client_read(client, &now);
            }
            if (FD_ISSET(client->fd, &wfds)) {
                handle_client_write(client);
            }
        }
        
        if (FD_ISSET(sockfd, &rfds)) {
            accept_client(sockfd);
        }

        handle_timers(&now);
    }
}
