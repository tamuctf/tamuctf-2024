# deployment vars
NAME := alien

all: $(NAME).elf

clean: .PHONY
	rm -f $(NAME).elf $(NAME).zip

build: Dockerfile Cargo.toml alien/ .cargo lm3s6965-uart flag.txt
	docker $(DOCKER_GLOBAL) build -t $(NAME) \
		--build-arg name=$(NAME) \
		.

extract: build
	$(eval id := $(shell docker create $(NAME)))
	docker cp $(id):/$(NAME)/$(NAME).elf - | tar xv $(NAME).elf
	docker rm -v $(id)

$(NAME).elf: extract

dist: extract
	zip $(NAME).zip $(NAME).elf

.PHONY:
