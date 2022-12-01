package applicationv1

import (
	"fmt"

	"github.com/urfave/cli/v2"
)

func (_self *ApplicationV1) _NewCommandServiceStart() (command *cli.Command) {
	command = &cli.Command{
		Name:        "service-start",
		Aliases:     []string{},
		Usage:       fmt.Sprintf("Start service - %s", "KCDE Sandbox"),
		Description: fmt.Sprintf("Start service - %s", "KCDE Sandbox"),
		Flags: []cli.Flag{
			&cli.StringFlag{Name: "controller_apiservice_host"},
			&cli.StringFlag{Name: "controller_apiservice_port"},
			&cli.StringFlag{Name: "controller_apiservice_proxy_v1_grpc_0_url"},
			&cli.StringFlag{Name: "controller_apiservice_proxy_v1_grpc_0_target_host"},
			&cli.StringFlag{Name: "controller_apiservice_proxy_v1_grpc_0_target_port"},
		},
		Action: _self._RunCommandActionServiceStart,
	}
	return command
}

func (_self *ApplicationV1) _RunCommandActionServiceStart(ctx *cli.Context) (err error) {
	func() {
		if ctx.String("controller_apiservice_host") != "" {
			_self.Configuration.Set("controller.apiservice.host", ctx.String("controller_apiservice_host"))
		}
		if ctx.String("controller_apiservice_port") != "" {
			_self.Configuration.Set("controller.apiservice.port", ctx.String("controller_apiservice_port"))
		}
		if ctx.String("controller_apiservice_proxy_v1_grpc_0_url") != "" {
			_self.Configuration.Set("controller.apiservice.proxy.v1.grpc.0.url", ctx.String("controller_apiservice_proxy_v1_grpc_0_url"))
		}
		if ctx.String("controller_apiservice_proxy_v1_grpc_0_target_host") != "" {
			_self.Configuration.Set("controller.apiservice.proxy.v1.grpc.0.target.host", ctx.String("controller_apiservice_proxy_v1_grpc_0_target_host"))
		}
		if ctx.String("controller_apiservice_proxy_v1_grpc_0_target_port") != "" {
			_self.Configuration.Set("controller.apiservice.proxy.v1.grpc.0.target.port", ctx.String("controller_apiservice_proxy_v1_grpc_0_target_port"))
		}

		//log.Printf("Overrided configuration from arguments - %+v", _self.Configuration)
	}()

	ch_err := make(chan error)
	go _self.ControllerApiService.Start(*_self.Context, ch_err)
	return <-ch_err
}
