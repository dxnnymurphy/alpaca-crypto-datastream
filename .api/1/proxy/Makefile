all: build

.PHONY: build
build: build-proto build-go

.PHONY: build-proto
build-proto:
	-cp -rf ../.model/.dist/go/* pkg/model/cryptodatastream/v3/
	cp -f pkg/model/cryptodatastream/v3/service-cryptodatastream.swagger.json pkg/resource/public/proxy/swagger/
	go mod tidy
	go mod vendor

.PHONY: build-go
build-go: build-go-api-proxy

.PHONY: build-go-%
build-go-%:
	mkdir -p .dist/bin
	go build -o .dist/bin ./cmd/$*/...

.PHONY: clean
clean: clean-go

.PHONY: clean-go
clean-go:
	rm -f pkg/model/cryptodatastream/v3/{*.pb.go,*.gw.go,*.swagger.json}
	rm -f pkg/resource/public/proxy/swagger/*.swagger.json
	rm -f go.sum
	rm -rf vendor
	rm -rf .dist/bin
	rm -rf .dist
