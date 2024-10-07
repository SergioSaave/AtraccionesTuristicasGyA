package routes

import "github.com/gorilla/mux"

func SetupIndexRoutes() *mux.Router {
	r := mux.NewRouter().StrictSlash(true)

	teacherRouter := r.PathPrefix("/teachers").Subrouter()
	SetupTeachersRoutes(teacherRouter)

	coursesRouter := r.PathPrefix("/courses").Subrouter()
	SetupCoursesRoutes(coursesRouter)

	sectionsRouter := r.PathPrefix("/sections").Subrouter()
	SetupSectionsRoutes(sectionsRouter)

	roomsRouter := r.PathPrefix("/rooms").Subrouter()
	SetupRoomsRoutes(roomsRouter)

	buildingsRouter := r.PathPrefix("/buildings").Subrouter()
	SetupBuildingsRoutes(buildingsRouter)

	schedulesRouter := r.PathPrefix("/schedules").Subrouter()
	SetupSchedulesRoutes(schedulesRouter)

	elasticRouter := r.PathPrefix("/elastic").Subrouter()
	SetupElasticRoutes(elasticRouter)

	return r
}
