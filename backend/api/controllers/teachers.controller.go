package controllers

import (
	"api_buscador/elastic"
	"bytes"
	"context"
	"net/http"
	"strings"

	"github.com/elastic/go-elasticsearch/v7/esutil"
	"github.com/gorilla/mux"
)

func GetTeachers(w http.ResponseWriter, r *http.Request) {
	es := elastic.GetClient()

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("teachers_index"),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var b bytes.Buffer
	b.ReadFrom(res.Body)
	w.Header().Set("Content-Type", "application/json")
	w.Write(b.Bytes())
}

func GetTeacherID(w http.ResponseWriter, r *http.Request) {

	id := strings.TrimPrefix(r.URL.Path, "/teachers/")

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"term": map[string]interface{}{
				"teacher_id": id,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("teachers_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var b bytes.Buffer
	b.ReadFrom(res.Body)
	w.Header().Set("Content-Type", "application/json")
	w.Write(b.Bytes())

}

func GetTeacherName(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	name := vars["name"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"teacher_name": name,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("teachers_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var b bytes.Buffer
	b.ReadFrom(res.Body)
	w.Header().Set("Content-Type", "application/json")
	w.Write(b.Bytes())

}
