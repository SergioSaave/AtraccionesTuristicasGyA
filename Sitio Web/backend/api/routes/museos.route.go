package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func SetupMuseosRoutes(router *mux.Router) {
	router.HandleFunc("/", controllers.MuseosHandler).Methods("GET")
}
