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

func GetRooms(w http.ResponseWriter, r *http.Request) {
	es := elastic.GetClient()

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("rooms_index"),
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

func GetRoomID(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/rooms/")

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"term": map[string]interface{}{
				"room_id": id,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("rooms_index"),
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

func GetRoomFloor(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	floor := vars["floor"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"term": map[string]interface{}{
				"floor": floor,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("rooms_index"),
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

func GetRoomName(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	room := vars["room"]

	es := elastic.GetClient()

	query := map[string]interface{}{
		"query": map[string]interface{}{
			"term": map[string]interface{}{
				"room": room,
			},
		},
	}

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("rooms_index"),
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
