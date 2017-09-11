CC = gcc

NAME = gydl

LIBS = -export-dynamic `pkg-config --libs gtk+-3.0`

FLAGS = -g -export-dynamic `pkg-config --cflags gtk+-3.0`

SRCS = src/gydl-download.c   \
       src/gydl-dialog.c     \
       src/gydl-window.c     \
       src/gydl-view.c       \
       src/main.c

all: $(SRCS)
	$(CC) $(FLAGS) $(SRCS) $(LIBS) -o $(NAME)

install: $(NAME)
	install -Dm 0755 $(NAME) /usr/bin/$(NAME)
	install -Dm 0644 data/com.github.JannikHv.Gydl.desktop /usr/share/applications/gydl.desktop
	install -Dm 0644 data/gydl.svg /usr/share/icons/gydl.svg
	install -Dm 0644 LICENSE /usr/share/licenses/gydl/LICENSE

uninstall:
	rm /usr/bin/$(NAME)
	rm /usr/share/applications/gydl.desktop
	rm /usr/share/icons/gydl.svg
	rm /usr/share/licenses/gydl/ -r

clean: $(NAME)
	rm $(NAME)
