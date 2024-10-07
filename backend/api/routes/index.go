package routes

import (
	"github.com/gorilla/mux"
)

func SetupIndexRoutes() *mux.Router {
	r := mux.NewRouter().StrictSlash(true)

	indexRouter := r.PathPrefix("/").Subrouter()
	IndexRoute(indexRouter)

	museumRouter := r.PathPrefix("/museos").Subrouter()
	SetupMuseumsRoutes(museumRouter)

	return r
}
