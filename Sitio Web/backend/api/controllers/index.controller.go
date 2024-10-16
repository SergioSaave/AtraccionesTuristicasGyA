package controllers

import (
	"encoding/json"
	"net/http"
)

type StatusResponse struct {
	Status string `json:"status"`
}

func IndexHandler(w http.ResponseWriter, r *http.Request) {
	// Crear la respuesta
	response := StatusResponse{
		Status: "ok",
	}

	// Configurar el tipo de contenido como JSON
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// Convertir la estructura a JSON y escribirla en la respuesta
	json.NewEncoder(w).Encode(response)
}
