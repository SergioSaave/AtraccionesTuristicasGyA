package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func SetupMonumentosRoutes(router *mux.Router) {
	router.HandleFunc("/", controllers.MonumentosHandler).Methods("GET")
}
