package application

import (
	"context"

	applicationv1 "dxnnymurphy.io/datastream/pkg/application/v1"
)

var (
	instances map[string]Application = make(map[string]Application)
)

func GetApplication(ctx context.Context, version string) (instance Application) {
	switch version {
	case "v1":
		if _, ok := instances["v1"]; !ok {
			instances["v1"] = applicationv1.NewApplicationV1(ctx)
		}
		instance = instances["v1"]
	default:
		instance = nil
	}
	return instance
}
