package main

import (
	"context"
	"log"
	"os"
	"os/signal"

	"dxnnymurphy.io/datastream/pkg/application"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, os.Interrupt)
	error_from_application := make(chan error)
	app := application.GetApplication(ctx, "v1")
	go app.Run(ctx, error_from_application)
	<-ch
	cancel()
	for {
		err := <-error_from_application
		if err != nil {
			log.Fatal(err)
			os.Exit(1)
		}
	}
}
