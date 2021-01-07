# C

## single

one process/thread with listen/accept. Throttling in pre-accepting queue
(backlog). Very bad performance (concurrency = 1)

## proc\_spawn

many workers (processes), each accepting connections. Good performance but we
need many workers (250) due to blocking api. Throttling in memory/process count
when many workers. Throttling in pre-accepting queue when there are few workers.

# NodeJS

## simple\_cluster.js

cluster solution. Master process accepting connections and send request to
workers (processes) through unix sockets. Processes uses non-blocking api but
throttle in CPU due to js probably. The nodejs doc states that this solution has
better balancing than the next scheme

## many\_accepts.js

hand-made cluster solution. Master process create server socket, spawn workers
and close socket. Workers listen/accept on common server socket. The nodejs doc
states that this solution can have good performance but has problems with
balancing. The balancing is OS job and OS do not have much information about
this usecase - if process can call accept syscall, then it can process tcp
connection even if his CPU is overloading. Due to async api using a process can
accept many connections and the full load is on this process.

# Golang

## server

simple server based on go-routines. The best solution - compiled code, use
threads for each cpu core and use coroutines.

# Apache httd

mpm variants - prefork, worker, event.

## prefork

it spawns workers as OS processes. The count of workers is small (~250) so
concurrency level maybe not so good for high load. This implementation is
similar to `c\_\_proc\_spawn`.

## worker

it is spawns workers as OS threads. The same as previous solution but have
lesser memory overhead on OS where a thread is lighter than a process.

## event

The same as previous two solution but have fix for keep-alive connections. In
case of keep-alive connections all workers can be in blocked state however they
are idle because http client do not send any requests. For simple connection
this variant is not better than previous two variants.
