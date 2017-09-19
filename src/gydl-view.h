#ifndef __GYDL_VIEW_H__
#define __GYDL_VIEW_H__

#include <gtk/gtk.h>

typedef struct _GydlView GydlView;

typedef enum {
        GYDL_VIEW_TYPE_AUDIO,
        GYDL_VIEW_TYPE_VIDEO,
} GydlViewType;

GtkWidget       *gydl_view_get_viewport (GydlView *view);

const gchar     *gydl_view_get_url      (GydlView *view);


const gchar     *gydl_view_get_format   (GydlView *view);

const gchar     *gydl_view_get_quality  (GydlView *view);

GydlView        *gydl_view_new          (GydlViewType view_type);

#endif /* __GYDL_VIEW_H__ */

/*
 * Editor modelines  -  https://www.wireshark.org/tools/modelines.html
 *
 * Local variables:
 * c-basic-offset: 8
 * tab-width: 8
 * indent-tabs-mode: nil
 * End:
 *
 * vi: set shiftwidth=8 tabstop=8 expandtab:
 * :indentSize=8:tabSize=8:noTabs=true:
 */
