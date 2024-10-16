package connections

import (
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var dsn = "host=localhost user=postgres password=password dbname=geodata port=5432"
var db *gorm.DB

func DBConnection() {
	var error error
	db, error = gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if error != nil {
		log.Fatal(error)
	} else {
		log.Println("Connected to Postgres.")
	}
}
