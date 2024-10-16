package controllers

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/url"
)

// ErrorResponse es la estructura para devolver errores en formato JSON
type ErrorResponse struct {
	Error string `json:"error"`
}

// ParksHandler maneja la ruta de parques y devuelve un JSON con la respuesta
func ParquesHandler(w http.ResponseWriter, r *http.Request) {
	// Define la URL base de Overpass API
	baseURL := "https://overpass-api.de/api/interpreter"

	// Define la consulta para los parques en las comunas específicas
	query := `
	[out:json];
	area["name"="Santiago"]["admin_level"="8"]->.santiago;
	area["name"="Providencia"]["admin_level"="8"]->.providencia;
	area["name"="Las Condes"]["admin_level"="8"]->.lascondes;
	area["name"="Ñuñoa"]["admin_level"="8"]->.nunoa;

	(
	  node["leisure"="park"](area.santiago);
	  node["leisure"="park"](area.providencia);
	  node["leisure"="park"](area.lascondes);
	  node["leisure"="park"](area.nunoa);
	  way["leisure"="park"](area.santiago);
	  way["leisure"="park"](area.providencia);
	  way["leisure"="park"](area.lascondes);
	  way["leisure"="park"](area.nunoa);
	);

	out body;
	>;
	out skel qt;
	`

	// Codifica la consulta para incluirla en la URL
	data := url.Values{}
	data.Set("data", query)

	// Haz la solicitud HTTP POST
	resp, err := http.PostForm(baseURL, data)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(ErrorResponse{Error: "Error en la solicitud a Overpass API"})
		return
	}
	defer resp.Body.Close()

	// Lee la respuesta
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(ErrorResponse{Error: "Error al leer la respuesta de Overpass API"})
		return
	}

	// Configurar el tipo de contenido como JSON
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// Enviar la respuesta JSON de Overpass API
	w.Write(body)
}
