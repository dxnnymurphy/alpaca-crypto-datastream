package authenticationbasicv1

import (
	"context"
	"crypto/subtle"
	"fmt"
	"net/http"

	"dxnnymurphy.io/cryptodatastream/pkg/configuration"
)

type AuthenticationBasicV1 struct {
	Configuration configuration.Configuration
}

func NewAuthenticationBasicV1(ctx context.Context) (instance *AuthenticationBasicV1) {
	instance = &AuthenticationBasicV1{
		Configuration: configuration.GetConfiguration(ctx, "v1"),
	}

	return instance
}

func (_self *AuthenticationBasicV1) EnableAuthenticationBasicForHttpHandler(ctx context.Context, profile string, handler http.Handler) (decorated_handler http.Handler) {
	profile_username := _self.Configuration.Get(fmt.Sprintf("security.authentication.basic.%s.username", profile)).(string)
	profile_password := _self.Configuration.Get(fmt.Sprintf("security.authentication.basic.%s.password", profile)).(string)

	decorated_handler = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		user, pass, ok := r.BasicAuth()
		if !ok || subtle.ConstantTimeCompare([]byte(user), []byte(profile_username)) != 1 || subtle.ConstantTimeCompare([]byte(pass), []byte(profile_password)) != 1 {
			w.Header().Set("WWW-Authenticate", "Basic realm=Please provide username and password")
			w.WriteHeader(401)
			w.Write([]byte("Unauthorised.\n"))
			return
		}

		handler.ServeHTTP(w, r)
	})
	return decorated_handler
}
