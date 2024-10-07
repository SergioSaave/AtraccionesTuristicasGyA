package controllers

import (
	"api_buscador/elastic"
	"bytes"
	"context"
	"net/http"

	"github.com/elastic/go-elasticsearch/v7/esutil"
	"github.com/gorilla/mux"
)

func GetSections(w http.ResponseWriter, r *http.Request) {
	es := elastic.GetClient()

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("sections_index"),
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

func GetSectionsSection(w http.ResponseWriter, r *http.Request) {

	vars := mux.Vars(r)
	section := vars["section"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"match": map[string]interface{}{
				"section": section,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("sections_index"),
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
