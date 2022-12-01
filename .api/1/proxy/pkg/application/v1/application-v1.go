package applicationv1

import (
	"context"
	"os"

	"github.com/urfave/cli/v2"
	"dxnnymurphy.io/cryptodatastream/pkg/configuration"
	controllerapiservice "dxnnymurphy.io/cryptodatastream/pkg/controller/apiservice"
)

type ApplicationV1 struct {
	Context              *context.Context
	Application          *cli.App
	Configuration        configuration.Configuration
	ControllerApiService controllerapiservice.ControllerApiService
}

func NewApplicationV1(ctx context.Context) (instance *ApplicationV1) {
	instance = &ApplicationV1{}

	instance.Context = &ctx
	instance.Configuration = configuration.GetConfiguration(ctx, "v1")
	instance.Application = instance._NewApp()
	instance.ControllerApiService = controllerapiservice.GetControllerApiService(ctx, "v1")

	return instance
}

func (_self *ApplicationV1) Run(ctx context.Context, err chan error) {
	err <- _self.Application.Run(os.Args)
}
