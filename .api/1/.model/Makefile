all: build

.PHONY: build
build: build-proto

.PHONY: build-proto
build-proto: build-proto-go build-proto-python 

.PHONY: build-proto-go
build-proto-go:
	cd src/model/cryptodatastream; \
		mkdir -p ./out; \
		protoc \
			-I. \
			-I$(HOME)/.danny/opt/github.com/googleapis/googleapis/current \
			-I$(HOME)/.danny/opt/github.com/grpc-ecosystem/grpc-gateway/current \
			--go_out=./out --go_opt=paths=source_relative \
			--go-grpc_out=./out --go-grpc_opt=paths=source_relative \
			--grpc-gateway_out=./out --grpc-gateway_opt=paths=source_relative --grpc-gateway_opt=logtostderr=true --grpc-gateway_opt generate_unbound_methods=true \
			--openapiv2_out=./out --openapiv2_opt=logtostderr=true \
			--experimental_allow_proto3_optional \
			./*.proto
	mkdir -p .dist/go; mv src/model/cryptodatastream/out/* .dist/go/
	rm -rf src/model/cryptodatastream/out

.PHONY: build-proto-python
build-proto-python:
	cd src/model/cryptodatastream; \
		mkdir -p ./out; \
		touch ./out/__init__.py; \
		python -m grpc_tools.protoc \
			-I. \
			-I$(HOME)/.danny/opt/github.com/googleapis/googleapis/current \
			-I$(HOME)/.danny/opt/github.com/grpc-ecosystem/grpc-gateway/current \
			--python_out=./out  --grpc_python_out=./out \
			--experimental_allow_proto3_optional \
			./*.proto 
	for FILE in `grep -Iin "^import.*_pb2.*" -R src/model/cryptodatastream/out | cut -f 1 -d ':' | sort -u`; do sed -i "s/^import.*_pb2.*/from . &/g" $$FILE; done
	mkdir -p .dist/python; mv src/model/cryptodatastream/out/* .dist/python/
	rm -rf src/model/cryptodatastream/out

.PHONY: clean
clean: clean-proto

.PHONY: clean-proto
clean-proto: clean-proto-go clean-proto-python
	rm -rf .dist

.PHONY: clean-proto-%
clean-proto-%:
	rm -rf .dist/$*
