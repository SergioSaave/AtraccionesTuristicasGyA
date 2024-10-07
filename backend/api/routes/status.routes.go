package routes

import (
	"encoding/json"
	"net/http"
)

func GetStatus(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"status": "ok",
		"routes": []string{
			"/",
			"/buildings",
			"/courses",
			"/rooms",
			"/schedules",
			"/sections",
			"/teachers",
		},
	}

	// Convertir el mapa a JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Establecer el encabezado de tipo de contenido a JSON
	w.Header().Set("Content-Type", "application/json")

	// Escribir la respuesta JSON
	w.Write(jsonResponse)
}
