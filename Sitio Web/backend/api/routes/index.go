package routes

import (
	"github.com/gorilla/mux"
)

func SetupIndexRoutes() *mux.Router {
	r := mux.NewRouter().StrictSlash(true)

	indexRouter := r.PathPrefix("/").Subrouter()
	IndexRoute(indexRouter)

	museosRouter := r.PathPrefix("/museos").Subrouter()
	SetupMuseosRoutes(museosRouter)

	iglesiasRouter := r.PathPrefix("/iglesias").Subrouter()
	SetupIglesiasRoutes(iglesiasRouter)

	monumentosRouter := r.PathPrefix("/monumentos").Subrouter()
	SetupMonumentosRoutes(monumentosRouter)

	parquesRouter := r.PathPrefix("/parques").Subrouter()
	SetupParquesRoutes(parquesRouter)

	return r
}
