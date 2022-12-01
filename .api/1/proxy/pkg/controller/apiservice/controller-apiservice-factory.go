package controllerapiservice

import (
	"context"

	controllerapiservicev1 "dxnnymurphy.io/cryptodatastream/pkg/controller/apiservice/v1"
)

var (
	instances map[string]ControllerApiService = make(map[string]ControllerApiService)
)

func GetControllerApiService(ctx context.Context, version string) (instance ControllerApiService) {
	switch version {
	case "v1":
		if _, ok := instances["v1"]; !ok {
			instances["v1"] = controllerapiservicev1.NewControllerApiServiceV1(ctx)
		}
		instance = instances["v1"]
	default:
		instance = nil
	}
	return instance
}
