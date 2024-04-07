NAME := jumbled

all: dist

clean: .PHONY
	rm -f $(NAME).zip

dist:
	zip $(NAME).zip private public flag.txt.enc

.PHONY: