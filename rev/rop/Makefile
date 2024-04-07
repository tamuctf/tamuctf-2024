# deployment vars
NAME := rop

CC := $(or $(CC),gcc)
CFLAGS := -fno-stack-protector -no-pie -static -w

$(NAME): $(NAME).c
	$(CC) $(CFLAGS) $^ -o $@
	python3 gen.py

clean: .PHONY
	rm -f $(NAME) $(NAME).zip

build: 
	docker $(DOCKER_GLOBAL) build -t $(NAME) .

extract: build
	$(eval id := $(shell docker create $(NAME)))
	docker cp $(id):/tmp/$(NAME) - | tar xv $(NAME)
	docker rm -v $(id)

dist: extract
	zip $(NAME).zip $(NAME)

.PHONY:
