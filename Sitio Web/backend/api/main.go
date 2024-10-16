package main

import (
	"api_rutas/connections"
	"api_rutas/routes"
	"log"
	"net/http"

	"github.com/gorilla/handlers"
)

func main() {
	connections.DBConnection()

	router := routes.SetupIndexRoutes()

	// Configurar CORS
	corsHandler := handlers.CORS(
		handlers.AllowedOrigins([]string{"*"}),
		handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}),
		handlers.AllowedHeaders([]string{"Content-Type", "Authorization"}),
	)(router)

	log.Println("Server running on port 4000")
	log.Fatal(http.ListenAndServe(":4000", corsHandler))
}
