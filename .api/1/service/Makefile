all: build

.PHONY: build
build: build-proto build-python

.PHONY: build-proto
build-proto:
	cp -rf ../.model/.dist/python/* src/kc/app/datastream/pkg/model/datastream/v3/

.PHONY: build-python
build-python:
	mkdir -p .dist/pkg/python
	pip wheel --wheel-dir=.dist/pkg/python .

.PHONY: install
install: install-python

.PHONY: install-python
install-python:
	pip install --force-reinstall .dist/pkg/python/datastream_api_service-*.whl

.PHONY: uninstall
uninstall: uninstall-python

.PHONY: uninstall-python
uninstall-python:
	pip uninstall -y datastream_api_service

.PHONY: clean
clean: clean-python

.PHONY: clean-python
clean-python:
	find . -name "__pycache__" -exec rm -rf {} +
	-rm -rf .dist/pkg/python
	-rm -rf .dist
	-rm -rf build
	-rm -f src/kc/app/datastream/pkg/model/datastream/v3/*.py
	-rm -rf src/datastream_*.egg-info
