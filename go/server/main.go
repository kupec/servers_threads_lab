package main

import (
	"fmt"
	"net/http"
)

func good(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "GOOD")
}

func main() {
	http.HandleFunc("/", good)

	http.ListenAndServe(":3001", nil)
}
