#####################################################################
### make init
#####################################################################

.PHONY: init
init: \
	init-pkg \
	init-go

.PHONY: init-pkg
init-pkg: \
	init-pkg-githubcom-googleapis-googleapis \
	init-pkg-githubcom-grpcecosystem/grpcgateway
                

.PHONY: init-pkg-githubcom-googleapis-googleapis
init-pkg-githubcom-googleapis-googleapis:
	mkdir -p $(HOME)/.danny/opt/github.com/googleapis/googleapis; \
		cd $(HOME)/.danny/opt/github.com/googleapis/googleapis; \
		curl -kL https://github.com/googleapis/googleapis/archive/873ab456273d105245df0fb82a6c17a814553b80.zip -O; \
		unzip -o 873ab456273d105245df0fb82a6c17a814553b80.zip; \
		ln -sfn googleapis-873ab456273d105245df0fb82a6c17a814553b80 current;

.PHONY: init-pkg-githubcom-grpcecosystem/grpcgateway
init-pkg-githubcom-grpcecosystem/grpcgateway:
	mkdir -p $(HOME)/.danny/opt/github.com/grpc-ecosystem/grpc-gateway; \
		cd $(HOME)/.danny/opt/github.com/grpc-ecosystem/grpc-gateway; \
		curl -kL https://github.com/grpc-ecosystem/grpc-gateway/archive/refs/tags/v2.11.2.zip -O; \
		unzip -o v2.11.2.zip; \
		ln -sfn grpc-gateway-2.11.2 current;

.PHONY: init-go
init-go: init-go-grpc

.PHONY: init-go-grpc
init-go-grpc:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2
	go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@v2.11.2
	go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@v2.11.2
	go install github.com/fullstorydev/grpcui/cmd/grpcui@v1.3.1

#####################################################################