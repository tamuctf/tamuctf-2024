# deployment vars
NAME := remote
FLAG := gigem{new_features_means_new_opportunities}

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
DOCKER_RUNTIME := --memory=128m --cpus=0.2 --restart=always --read-only --tmpfs /tmp --tmpfs /run --tmpfs /var/log/apache2


# ============================================================
# NOTE: if not compiling, the $(NAME) dep along with compilation
# 	directive can be safely removed
#	docker directives may be removed if docker is not used
#	dist directives should be omitted if there is no distributable
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
	zip -r $(NAME).zip src/static/ src/bulletproof.php src/index.php src/favicon.ico

.PHONY:
