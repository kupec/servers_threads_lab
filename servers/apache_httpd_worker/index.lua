require "string"

function handle(r)
    r.usleep(100000)
    r.content_type = "text/plain"
    r:puts("GOOD")
    return apache2.OK
end
