package models

import (
	"gorm.io/gorm"
)

type Museo struct {
	gorm.Model
	Geom       string `gorm:"type:geometry"`
	Properties string `gorm:"type:jsonb"`
}
