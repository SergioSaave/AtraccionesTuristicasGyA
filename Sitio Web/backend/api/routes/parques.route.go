package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func SetupParquesRoutes(router *mux.Router) {
	router.HandleFunc("/", controllers.ParquesHandler).Methods("GET")
}
