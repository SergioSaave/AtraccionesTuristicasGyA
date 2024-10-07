package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupTeachersRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetTeachers).Methods("GET")
	router.HandleFunc("/{id}", controllers.GetTeacherID).Methods("GET")
	router.HandleFunc("/name/{name}", controllers.GetTeacherName).Methods("GET")

}
