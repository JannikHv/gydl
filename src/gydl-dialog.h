#ifndef __GYDL_DIALOG_H__
#define __GYDL_DIALOG_H__

#include <gtk/gtk.h>

typedef struct _GydlDialog GydlDialog;

typedef enum {
        GYDL_DIALOG_TYPE_NET_ERROR,
        GYDL_DIALOG_TYPE_DL_ERROR,
        GYDL_DIALOG_TYPE_DL_FINISH,
} GydlDialogType;

GtkWidget       *gydl_dialog_get_window (GydlDialog *dialog);

GydlDialog      *gydl_dialog_new        (GydlDialogType dialog_type);

#endif /* __GYDL_DIALOG_H__ */

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
