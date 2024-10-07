package main

import (
	"api_rutas/connections"
	"api_rutas/routes"
	"log"
	"net/http"
)

func main() {
	connections.DBConnection()

	router := routes.SetupIndexRoutes()

	log.Println("Server running on port 4000")
	log.Fatal(http.ListenAndServe(":4000", router))
}
