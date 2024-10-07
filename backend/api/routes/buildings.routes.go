package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupBuildingsRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetBuildings).Methods("GET")
	router.HandleFunc("/{id}", controllers.GetBuildingID).Methods("GET")
	router.HandleFunc("/address/{address}", controllers.GetBuildingAddress).Methods("GET")

}
