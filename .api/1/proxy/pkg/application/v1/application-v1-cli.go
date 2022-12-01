package applicationv1

import (
	"os"

	"github.com/urfave/cli/v2"
)

func (_self *ApplicationV1) _NewApp() (app *cli.App) {
	app = &cli.App{
		Name:        "kcde-api-proxy",
		Usage:       "KCDE API Proxy",
		Description: "KCDE API Proxy",
		Authors: []*cli.Author{
			{
				Name:  "Tama MA",
				Email: "pma@keplercheuvreux.com",
			},
		},
		Flags:  []cli.Flag{},
		Action: _self._RunAction,
	}

	app.Commands = []*cli.Command{
		_self._NewCommandServiceStart(),
	}

	return app
}

func (_self *ApplicationV1) _RunAction(ctx *cli.Context) (err error) {
	switch {
	default:
		cli.ShowAppHelp(ctx)
	}
	os.Exit(0)
	return err
}
