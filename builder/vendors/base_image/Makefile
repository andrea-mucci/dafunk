.PHONY: init-local root all start boot extract image

all: root extract image

export arch="$(uname -m)"

# init-local builds a static binary for local testing, but the lab uses a multi-stage
# Dockerfile for this instead - https://docs.docker.com/develop/develop-images/multistage-build/
init-local:
	cd init && \
	go build --tags netgo --ldflags '-s -w -extldflags "-lm -lstdc++ -static"' -o init main.go

root:
	docker build -t alexellis2/custom-init .

# Get the AWS sample image
# change to Image when using aarch64, instead of vmlinux.bin
kernel:
	latest = wget "http://spec.ccfc.min.s3.amazonaws.com/?prefix=firecracker-ci/v1.11/x86_64/vmlinux-5.10&list-type=2" -O - 2>/dev/null | grep -oP "(?<=<Key>)(firecracker-ci/v1.11/x86_64/vmlinux-5\.10\.[0-9]{1,3})(?=</Key>)" ;\
	echo $latest ;\
	curl -o vmlinux -S -L "https://s3.amazonaws.com/spec.ccfc.min/$$LATEST" ;\

# Extract a root filesystem into a tar
extract:
	docker rm -f extract || :
	rm -rf rootfs.tar || :
	docker create --name extract alexellis2/custom-init
	docker export extract -o rootfs
	docker rm -f extract

# Allocate a 5GB disk image, then extract the rootfs.tar from the
# container into it
image:
	set -e
	rm -rf rootfs.img || : ;\
	sudo fallocate -l 5G ./rootfs.img  ;\
	sudo mkfs.ext4 ./rootfs.img  ;\
	TMP=$$(mktemp -d)  ;\
	echo $$TMP  ;\
	sudo mount -o loop ./rootfs.img $$TMP  ;\
	sudo tar -xvf rootfs.tar -C $$TMP  ;\
	sudo umount $$TMP

# Start a firecracker process, ready for commands
start:
	sudo rm -f /tmp/firecracker.socket || :
	sudo firecracker --api-sock /tmp/firecracker.socket

# Sends commands to boot the firecracker process started via "make start"
boot:
	 sudo ./boot.sh