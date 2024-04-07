# deployment vars
NAME := cracked
FLAG := $(shell cat flag.txt)
KEY := 6lmao9

# ============================================================
# NOTE: the following are only necessary if hosting containers
# This can be safely removed
# ============================================================

REGISTRY :=
SUFFIX :=

# configurable vars:
# HPORTS="8888 8889" make -e ...
CPORTS := 8000
HPORTS := $(CPORTS)
SERVICES := HTTP

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
DOCKER_RUNTIME := --memory=128m --cpus=0.2 --read-only --restart=always


# ============================================================
# NOTE: if not compiling, the $(NAME) dep along with compilation
# 	directive can be safely removed
# ============================================================

clean: .PHONY
	docker container rm -f $(NAME)$(SUFFIX)

build: Dockerfile
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg key=$(KEY) \
		--build-arg flag=$(FLAG) \
		--build-arg port=$(HTTP_CPORT) \
		.

run:
	$(eval ports := $(shell python -c "for h, c in zip('$(HPORTS)'.split(), '$(CPORTS)'.split()): print(f' -p {h}:{c}')"))
	docker $(DOCKER_GLOBAL) run $(DOCKER_RUNTIME) -d --name $(NAME)$(SUFFIX) $(ports) $(REGISTRY)$(NAME)

.PHONY:
