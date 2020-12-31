package main

import (
	"fmt"
	"net/http"
	"time"
)

func good(w http.ResponseWriter, req *http.Request) {
	time.Sleep(100 * time.Millisecond)
	fmt.Fprintf(w, "GOOD")
}

func main() {
	http.HandleFunc("/", good)

	http.ListenAndServe(":3001", nil)
}
