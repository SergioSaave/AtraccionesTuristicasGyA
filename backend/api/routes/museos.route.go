package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func SetupMuseumsRoutes(router *mux.Router) {
	router.HandleFunc("/", controllers.MuseumsHandler).Methods("GET")
}
