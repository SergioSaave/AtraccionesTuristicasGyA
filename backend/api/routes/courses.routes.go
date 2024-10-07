package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupCoursesRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetCourses).Methods("GET")
	router.HandleFunc("/{name}", controllers.GetCourseName).Methods("GET")
	router.HandleFunc("/code/{code}", controllers.GetCourseCode).Methods("GET")

}
