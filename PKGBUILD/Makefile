:BINARY:=mc-serve

all: uninstall install clean

.PHONY: clean
clean:
	@echo "Cleaning build files..."
	@rm -f *.pkg.tar.xz
	@rm -rf pkg src
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@echo "Done."

.PHONY: checksum
checksum:
	@updpkgsums ./PKGBUILD

.PHONY: build
build:
	@updpkgsums ./PKGBUILD
	@makepkg -fpL ./PKGBUILD --noconfirm

.PHONY: install
install:
	@updpkgsums ./PKGBUILD
	@makepkg -Ccip ./PKGBUILD --noconfirm

.PHONY: uninstall
uninstall:
	@sudo pacman -R $(BINARY) --noconfirm 