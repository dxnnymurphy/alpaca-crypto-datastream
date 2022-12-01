package resource

import (
	"embed"
)

var (
	//go:embed config/application.yml
	ConfigApplicationYml []byte

	//go:embed public/proxy/swagger
	PublicProxySwagger embed.FS
)
