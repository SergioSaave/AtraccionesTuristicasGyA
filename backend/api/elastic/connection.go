package elastic

import (
	"log"

	"github.com/elastic/go-elasticsearch/v7"
)

// Client is a global variable to hold the Elasticsearch client
var Client *elasticsearch.Client

// InitializeClient initializes the Elasticsearch client and assigns it to the Client variable
func InitializeClient() {
	cfg := elasticsearch.Config{
		Addresses: []string{
			"http://localhost:9200",
		},
	}

	es, err := elasticsearch.NewClient(cfg)
	if err != nil {
		log.Fatalf("Error creating the client: %s", err)
	}

	res, err := es.Info()
	if err != nil {
		log.Fatalf("Error getting response: %s", err)
	}
	defer res.Body.Close()

	log.Println(res)

	Client = es
}

// GetClient returns the Elasticsearch client
func GetClient() *elasticsearch.Client {
	return Client
}
