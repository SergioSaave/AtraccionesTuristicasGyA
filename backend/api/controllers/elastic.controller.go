package controllers

import (
	"api_buscador/elastic"
	"api_buscador/models"
	"context"
	"encoding/json"
	"net/http"

	"github.com/elastic/go-elasticsearch/v7/esutil"
	"github.com/gorilla/mux"
)

func GetAll(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	word := vars["word"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"word": word,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("word_list_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var esResponse models.ElasticResponse
	if err := json.NewDecoder(res.Body).Decode(&esResponse); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var sources []map[string]interface{}
	for _, hit := range esResponse.Hits.Hits {
		sources = append(sources, hit.Source)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(sources)
}

func GetByCourses(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	name := vars["name"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"course": name,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("salas_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var esResponse models.ElasticResponse
	if err := json.NewDecoder(res.Body).Decode(&esResponse); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var sources []map[string]interface{}
	for _, hit := range esResponse.Hits.Hits {
		sources = append(sources, hit.Source)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(sources)
}

func GetByTeachers(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	name := vars["name"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"teacher": name,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("salas_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var esResponse models.ElasticResponse
	if err := json.NewDecoder(res.Body).Decode(&esResponse); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var sources []map[string]interface{}
	for _, hit := range esResponse.Hits.Hits {
		sources = append(sources, hit.Source)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(sources)
}

func GetByID(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"id": id,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("salas_index"),
		es.Search.WithBody(esutil.NewJSONReader(&query)),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var esResponse models.ElasticResponse
	if err := json.NewDecoder(res.Body).Decode(&esResponse); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var sources []map[string]interface{}
	for _, hit := range esResponse.Hits.Hits {
		sources = append(sources, hit.Source)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(sources)
}
