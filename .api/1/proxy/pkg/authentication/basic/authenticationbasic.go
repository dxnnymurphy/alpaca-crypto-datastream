package authenticationbasic

import (
	"context"
	"net/http"
)

type AuthenticationBasic interface {
	EnableAuthenticationBasicForHttpHandler(ctx context.Context, profile string, handler http.Handler) (decorated_handler http.Handler)
}
