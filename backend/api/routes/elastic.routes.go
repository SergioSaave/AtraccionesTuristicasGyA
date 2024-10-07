package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupElasticRoutes(router *mux.Router) {
	router.HandleFunc("/all/{word}", controllers.GetAll).Methods("GET")
	router.HandleFunc("/courses/{name}", controllers.GetByCourses).Methods("GET")
	router.HandleFunc("/teachers/{name}", controllers.GetByTeachers).Methods("GET")
	router.HandleFunc("/{id}", controllers.GetByID).Methods("GET")
}
