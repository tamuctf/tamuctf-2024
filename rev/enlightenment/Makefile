# deployment vars
NAME := enlightenment

all: $(NAME)

clean: .PHONY
	rm -f $(NAME) $(NAME).zip

build: Dockerfile src Cargo.toml
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg name=$(NAME) \
		.

extract:
	$(eval id := $(shell docker create $(NAME)))
	docker cp $(id):/$(NAME)/target/release/$(NAME) - | tar xv $(NAME)
	docker rm -v $(id)

$(NAME): build extract

dist: extract
	zip $(NAME).zip $(NAME)

.PHONY:
