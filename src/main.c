#include "gydl-window.h"

#include <gtk/gtk.h>

gint main(gint argc,
          gchar *argv[])
{
        gtk_init(&argc, &argv);

        GydlWindow *win;

        win = gydl_window_new();

        gydl_window_show_all(win);

        gtk_main();
}
