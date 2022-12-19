package configuration

import (
	"context"

	configurationv1 "dxnnymurphy.io/datastream/pkg/configuration/v1"
)

var (
	instances map[string]Configuration = make(map[string]Configuration)
)

func GetConfiguration(ctx context.Context, version string) (instance Configuration) {
	switch version {
	case "v1":
		if _, ok := instances["v1"]; !ok {
			instances["v1"] = configurationv1.NewConfigurationV1(ctx)
		}
		instance = instances["v1"]
	default:
		instance = nil
	}
	return instance
}
