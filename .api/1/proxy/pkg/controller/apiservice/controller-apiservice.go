package controllerapiservice

import "context"

type ControllerApiService interface {
	Start(ctx context.Context, err chan error)
}
