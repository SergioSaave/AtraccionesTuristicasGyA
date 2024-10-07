package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func SetupIglesiasRoutes(router *mux.Router) {
	router.HandleFunc("/", controllers.IglesiasHandler).Methods("GET")
}
