package authenticationbasic

import (
	"context"

	authenticationbasicv1 "dxnnymurphy.io/datastream/pkg/authentication/basic/v1"
)

var (
	instances map[string]AuthenticationBasic = make(map[string]AuthenticationBasic)
)

func GetAuthenticationBasic(ctx context.Context, version string) (instance AuthenticationBasic) {
	switch version {
	case "v1":
		if _, ok := instances["v1"]; !ok {
			instances["v1"] = authenticationbasicv1.NewAuthenticationBasicV1(ctx)
		}
		instance = instances["v1"]
	default:
		instance = nil
	}
	return instance
}
