package main

import (
	"log"
	"net/http"

	"api_buscador/elastic"
	"api_buscador/routes"
)

func main() {
	elastic.InitializeClient()


	router := routes.SetupIndexRoutes()
  
	log.Println("Server running on port 4000")
	log.Fatal(http.ListenAndServe(":4000", router))
}
