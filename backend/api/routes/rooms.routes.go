package routes

import (
	"api_buscador/controllers"

	"github.com/gorilla/mux"
)

func SetupRoomsRoutes(router *mux.Router) {

	router.HandleFunc("/all", controllers.GetRooms).Methods("GET")
	router.HandleFunc("/{id}", controllers.GetRoomID).Methods("GET")
	router.HandleFunc("/floor/{floor}", controllers.GetRoomFloor).Methods("GET")
	router.HandleFunc("/room/{room}", controllers.GetRoomName).Methods("GET")
}
