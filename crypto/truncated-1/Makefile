NAME := truncated-1

all: dist

clean: .PHONY
	rm -f $(NAME).zip

dist:
	zip $(NAME).zip private.pem public.pem flag.txt.enc

.PHONY:
