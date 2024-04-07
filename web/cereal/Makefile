# deployment vars
NAME := cereal
FLAG := gigem{c3r3aL_t0o_sWe3t_t0d2y}

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
SERVICES := SITE

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
DOCKER_RUNTIME := --memory=128m --cpus=0.2 --restart=always


# ============================================================
# NOTE: if not compiling, the $(NAME) dep along with compilation
# 	directive can be safely removed
# ============================================================

# build vars
clean: .PHONY
	docker container rm -f $(NAME)$(SUFFIX)
	rm -f $(NAME).zip

build: Dockerfile
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg flag=$(FLAG) \
		--build-arg port=$(SITE_CPORT) \
		.

run:
	$(eval ports := $(shell python -c "for h, c in zip('$(HPORTS)'.split(), '$(CPORTS)'.split()): print(f' -p {h}:{c}')"))
	docker $(DOCKER_GLOBAL) run $(DOCKER_RUNTIME) -d --name $(NAME)$(SUFFIX) $(ports) $(REGISTRY)$(NAME)

dist:
	zip -r $(NAME).zip src/

.PHONY:
