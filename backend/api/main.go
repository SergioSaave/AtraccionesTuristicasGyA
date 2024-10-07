package main

import (
	"api_rutas/connections"
	"api_rutas/routes"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	connections.DBConnection()

	r := mux.NewRouter()

	r.HandleFunc("/", routes.HomeHandler)

	http.ListenAndServe(":3000", r)
}
