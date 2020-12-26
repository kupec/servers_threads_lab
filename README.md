# single
one process/thread with listen/accept. Throttling in pre-accepting queue

# proc\_spawn
many workers (processes), each accepting connections. Good performance but we need more workers due to blocking api. Throttling in memory/process count when many workers. Throttling in pre-accepting queue when few workers.

# simple\_cluster.js
cluster solution. Master process accepting connections and send request to workers (processes) through unix sockets. Processes uses non-blocking api but throttle in CPU due to js probably. The nodejs doc states that this solution has better balancing than next scheme

# many\_accepts.js
hand-mane cluster solution. Master process create server socket, spawn workers and close socket. Workers listen/accept on common server socket. The nodejs doc states that this solution has good performance but has problems with balancing. Because it is OS job and OS do not have much information about this usecase - if process can call accept syscall, then it can process tcp connection even if his CPU is overloading.
