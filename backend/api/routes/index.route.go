package routes

import (
	"api_rutas/controllers"

	"github.com/gorilla/mux"
)

func IndexRoute(router *mux.Router) {
	router.HandleFunc("/", controllers.IndexHandler).Methods("GET")
}
