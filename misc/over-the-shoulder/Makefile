# deployment vars
NAME := over-the-shoulder

# ============================================================
# NOTE: the following are only necessary if hosting containers
# This can be safely removed
# ============================================================

REGISTRY :=
SUFFIX :=

# configurable vars:
# HPORTS="8888 8889" make -e ...
CPORTS := 5000
HPORTS := $(CPORTS)
SERVICES := QEMU

# generate service -> port mappings: SERVICE_PORT := PORT
# this is necessary for docker compose string substitution via env variables
# also useful for containers requiring build args for setting ports on multiple services
$(foreach var, \
    $(shell \
				python -c "for s, p in zip('$(SERVICES)'.split(), '$(CPORTS)'.split()): print(f'{s}_CPORT:={p}')" \
    ), $(eval $(var)) \
)

# docker
DOCKER_CONTEXT := default
DOCKER_GLOBAL := --context $(DOCKER_CONTEXT)
# Read-only is managed within the container by jailing
# Privileged is required for jailing + KVM
# Memory is cheap, QEMU is not; please increase this later
DOCKER_RUNTIME := --memory=8g --cpus=8 --restart=always --privileged

all: build

clean:
	rm -rf $(NAME).zip
	docker container rm -f $(NAME)$(SUFFIX)

build: .PHONY
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg name=$(NAME) \
		.

run:
	$(eval ports := $(shell python -c "for h, c in zip('$(HPORTS)'.split(), '$(CPORTS)'.split()): print(f' -p {h}:{c}')"))
	docker $(DOCKER_GLOBAL) run $(DOCKER_RUNTIME) -d --name $(NAME)$(SUFFIX) $(ports) $(REGISTRY)$(NAME)

stop:
	docker $(DOCKER_GLOBAL) rm -f $(NAME)$(SUFFIX)

dist:
	zip $(NAME).zip solver-template.py

.PHONY:
