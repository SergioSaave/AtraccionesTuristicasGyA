package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupSectionsRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetSections).Methods("GET")
	router.HandleFunc("/{section}", controllers.GetSections).Methods("GET")

}
