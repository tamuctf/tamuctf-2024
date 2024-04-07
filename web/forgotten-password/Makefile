# deployment vars
NAME := forgotten-password
FLAG := gigem{sptfy.com/Qhnv}
MAILGUN_API_KEY := b44b673206d93bea8a56ac219b0edadf-f68a26c9-efa80883
RAILS_MASTER_KEY := 6a2e12f511702b69c7f6860c4478c7ce

# ============================================================
# NOTE: the following are only necessary if hosting containers
# This can be safely removed
# ============================================================

REGISTRY :=
SUFFIX :=

# configurable vars:
# HPORTS="8888 8889" make -e ...
CPORTS := 3000
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
DOCKER_RUNTIME := --memory=1g --cpus=0.7 --restart=always


# ============================================================
# NOTE: if not compiling, the $(NAME) dep along with compilation
#     directive can be safely removed
#    docker directives may be removed if docker is not used
#    dist directives should be omitted if there is no distributable
# ============================================================

clean: .PHONY
	rm -f $(NAME).zip
	docker container rm -f $(NAME)$(SUFFIX)

build: Dockerfile
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
	--build-arg http_port=$(HTTP_CPORT) \
	--build-arg mailgun_api_key=$(MAILGUN_API_KEY) \
	--build-arg rails_master_key=$(RAILS_MASTER_KEY) \
	--build-arg flag=$(FLAG) \
        .

run:
	$(eval ports := $(shell python -c "for h, c in zip('$(HPORTS)'.split(), '$(CPORTS)'.split()): print(f' -p {h}:{c}')"))
	docker $(DOCKER_GLOBAL) run $(DOCKER_RUNTIME) -d --name $(NAME)$(SUFFIX) $(ports) $(REGISTRY)$(NAME)

dist:
	zip -r $(NAME).zip src/

.PHONY:
