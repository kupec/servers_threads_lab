# servers differences

see servers/README.md

# http load

- http/1.1 keep-alive. If load generator uses 10 concurrent connections it means there are 10 tcp connections which are reused many times. Without keep-alive we can create many tcp connections and waste ephemeral ports on client machine (it cannot be set more than 64k due to tcp packet field)
