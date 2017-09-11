#ifndef __GYDL_WINDOW_H__
#define __GYDL_WINDOW_H__

#include <gtk/gtk.h>

typedef struct _GydlWindow GydlWindow;

void             gydl_window_show_all   (GydlWindow *win);

GydlWindow      *gydl_window_new        (void);

#endif /* __GYDL_WINDOW_H__ */
