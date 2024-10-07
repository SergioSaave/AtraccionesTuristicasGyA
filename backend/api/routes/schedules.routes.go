package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupSchedulesRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetSchedules).Methods("GET")

}
