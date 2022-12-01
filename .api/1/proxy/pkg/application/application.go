package application

import "context"

type Application interface {
	Run(ctx context.Context, err chan error)
}
