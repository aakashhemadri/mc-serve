:BINARY:=mc-serve

all: clean build install

.PHONY: clean
clean:
	@echo "Cleaning build files..."
	@rm -f *.pkg.tar.xz
	@rm -rf pkg src
	@rm -rf build
	@rm -rf dist
	@rm -rf bin
	@rm -rf *.egg-info
	@echo "Done."

.PHONY: build
build:
	@python setup.py sdist bdist_wheel

.PHONY: install
install:
	@python setup.py install

.PHONY: upload-test
upload-test: build
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*