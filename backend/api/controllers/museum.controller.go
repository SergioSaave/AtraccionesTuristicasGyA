package controllers

import (
	"api_rutas/models"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"

	"gorm.io/gorm"
)

var db *gorm.DB

func GetMuseum(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Welcome to the museum page."))
}

func MuseumsHandler(w http.ResponseWriter, r *http.Request) {
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
		http.Error(w, "Error en la solicitud a Overpass API", http.StatusInternalServerError)
		fmt.Println("Error en la solicitud:", err)
		return
	}
	defer resp.Body.Close()

	// Lee la respuesta
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error al leer la respuesta de Overpass API", http.StatusInternalServerError)
		fmt.Println("Error al leer la respuesta:", err)
		return
	}

	// Inserta el GeoJSON en la base de datos usando GORM
	err = saveGeoJSONToPostGIS(body)
	if err != nil {
		http.Error(w, "Error al insertar GeoJSON en PostGIS", http.StatusInternalServerError)
		fmt.Println("Error al insertar GeoJSON en PostGIS:", err)
		return
	}

	// Enviar la respuesta al cliente
	w.Header().Set("Content-Type", "application/json")
	w.Write(body)
}

// saveGeoJSONToPostGIS inserta los datos GeoJSON en la base de datos PostGIS usando GORM
func saveGeoJSONToPostGIS(geojsonData []byte) error {
	// Parsear el GeoJSON
	var featureCollection map[string]interface{}
	err := json.Unmarshal(geojsonData, &featureCollection)
	if err != nil {
		return fmt.Errorf("error parsing GeoJSON: %v", err)
	}

	features := featureCollection["features"].([]interface{})
	for _, feature := range features {
		featureMap := feature.(map[string]interface{})

		// Extraer la geometría y las propiedades del feature
		geom, err := json.Marshal(featureMap["geometry"])
		if err != nil {
			return fmt.Errorf("error marshalling geometry: %v", err)
		}

		properties, err := json.Marshal(featureMap["properties"])
		if err != nil {
			return fmt.Errorf("error marshalling properties: %v", err)
		}

		// Insertar los datos en la base de datos usando GORM y PostGIS
		museo := models.Museo{
			Geom:       string(geom), // Almacenar la geometría como GeoJSON
			Properties: string(properties),
		}

		// Usa una consulta personalizada para insertar la geometría en formato GeoJSON
		err = db.Exec(`
			INSERT INTO museos (geom, properties)
			VALUES (
				ST_SetSRID(ST_GeomFromGeoJSON(?), 4326), ?
			)
		`, museo.Geom, museo.Properties).Error
		if err != nil {
			return fmt.Errorf("error inserting museum into database: %v", err)
		}
	}

	fmt.Println("GeoJSON insertado en PostGIS usando GORM")
	return nil
}
