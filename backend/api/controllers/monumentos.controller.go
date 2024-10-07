package controllers

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
)

func MonumentosHandler(w http.ResponseWriter, r *http.Request) {
	// Define la URL base de Overpass API
	baseURL := "https://overpass-api.de/api/interpreter"

	// Define la consulta con el bounding box y los filtros
	query := `
	[out:json][timeout:25];
	nwr["tourism"="museum"](bbox);
	out geom;
	`

	// Define las coordenadas del bounding box
	minLat := -33.54912050860342 // Límite sur
	minLon := -70.79795837402345 // Límite oeste
	maxLat := -33.35834837283271 // Límite norte
	maxLon := -70.52639007568361 // Límite este

	// Reemplaza {{bbox}} con las coordenadas en la consulta
	query = fmt.Sprintf(`
	[out:json][timeout:25];
	nwr["tourism"="museum"](%.6f,%.6f,%.6f,%.6f);
	out geom;
	`, minLat, minLon, maxLat, maxLon)

	// Codifica la consulta para incluirla en la URL
	data := url.Values{}
	data.Set("data", query)

	// Haz la solicitud HTTP POST
	resp, err := http.PostForm(baseURL, data)
	if err != nil {
		fmt.Println("Error en la solicitud:", err)
		return
	}
	defer resp.Body.Close()

	// Lee la respuesta
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error al leer la respuesta:", err)
		return
	}

	// Configurar el tipo de contenido como JSON
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// Enviar la respuesta JSON de Overpass API
	w.Write(body)
}
