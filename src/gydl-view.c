#include "gydl-view.h"

#include <gtk/gtk.h>

struct _GydlView  {
        /* Containers */
        GtkWidget *self;

        /* Labels */
        GtkWidget *l_entry;
        GtkWidget *l_format;
        GtkWidget *l_quality;

        /* Widgets */
        GtkWidget *entry;
        GtkWidget *cb_format;
        GtkWidget *cb_quality;

        /* Type */
        GydlViewType type;
};

static void gydl_audio_view_init(GydlView *view)
{
        gint i;
        const gchar *format[5] = {"aac", "m4a", "mp3", "vorbis", "wav"};
        const gchar *quality[10] = {
                "0 (best)", "1", "2", "3", "4",
                "5", "6", "7", "8", "9 (worst)"
        };

        for (i = 0; i < 5; i++)
                gtk_combo_box_text_append_text(GTK_COMBO_BOX_TEXT(view->cb_format),
                                               format[i]);

        for (i = 0; i < 10; i++)
                gtk_combo_box_text_append_text(GTK_COMBO_BOX_TEXT(view->cb_quality),
                                               quality[i]);

        gtk_combo_box_set_active(GTK_COMBO_BOX(view->cb_format), 2);
        gtk_combo_box_set_active(GTK_COMBO_BOX(view->cb_quality), 5);
}

static void gydl_video_view_init(GydlView *view)
{
        gint i;
        const gchar *format[4] = {"3gp", "flv", "mp4", "webm"};
        const gchar *quality[8] = {
                "2160p", "1440p", "1080p", "720p",
                "480p", "360p", "240p", "144p"
        };

        for (i = 0; i < 4; i++)
                gtk_combo_box_text_append_text(GTK_COMBO_BOX_TEXT(view->cb_format),
                                               format[i]);

        for (i = 0; i < 8; i++)
                gtk_combo_box_text_append_text(GTK_COMBO_BOX_TEXT(view->cb_quality),
                                               quality[i]);

        gtk_combo_box_set_active(GTK_COMBO_BOX(view->cb_format), 2);
        gtk_combo_box_set_active(GTK_COMBO_BOX(view->cb_quality), 3);
}

static void gydl_view_init(GydlView *view)
{
        view->self = gtk_grid_new();

        view->l_entry   = gtk_label_new(NULL);
        view->l_format  = gtk_label_new(NULL);
        view->l_quality = gtk_label_new(NULL);

        view->entry      = gtk_entry_new();
        view->cb_format  = gtk_combo_box_text_new();
        view->cb_quality = gtk_combo_box_text_new();

        /* Grid */
        gtk_grid_set_column_homogeneous(GTK_GRID(view->self), TRUE);
        gtk_container_set_border_width(GTK_CONTAINER(view->self), 10);

        /* Labels */
        gtk_label_set_markup(GTK_LABEL(view->l_entry),
                             "<span size='15000'><u>\nEnter the URL\n</u></span>");
        gtk_label_set_markup(GTK_LABEL(view->l_format),
                            "<span size='15000'><u>\nFormat\n</u></span>");
        gtk_label_set_markup(GTK_LABEL(view->l_quality),
                             "<span size='15000'><u>\nQuality\n</u></span>");

        /* Entry */
        gtk_entry_set_placeholder_text(GTK_ENTRY(view->entry),
                                       "https://youtube.com/watch...");

        /* Combo boxes */
        gtk_container_set_border_width(GTK_CONTAINER(view->cb_format), 5);
        gtk_container_set_border_width(GTK_CONTAINER(view->cb_quality), 5);

        /* Attach widgets to grid */
        gtk_grid_attach(GTK_GRID(view->self), view->l_entry, 0, 0, 4, 1);
        gtk_grid_attach(GTK_GRID(view->self), view->entry, 0, 1, 4, 1);
        gtk_grid_attach(GTK_GRID(view->self), view->l_format, 0, 2, 2, 1);
        gtk_grid_attach(GTK_GRID(view->self), view->l_quality, 2, 2, 2, 1);
        gtk_grid_attach(GTK_GRID(view->self), view->cb_format, 0, 3, 2, 1);
        gtk_grid_attach(GTK_GRID(view->self), view->cb_quality, 2, 3, 2, 1);

        switch (view->type) {
        case GYDL_VIEW_TYPE_AUDIO:
                gydl_audio_view_init(view);
                break;
        case GYDL_VIEW_TYPE_VIDEO:
                gydl_video_view_init(view);
                break;
        default:
                break;
        }
}

/**
 * Accessors
 */
GtkWidget *gydl_view_get_viewport(GydlView *view)
{
        return view->self;
}

const gchar *gydl_view_get_url(GydlView *view)
{
        return gtk_entry_get_text(GTK_ENTRY(view->entry));
}

const gchar *gydl_view_get_format(GydlView *view)
{
        return gtk_combo_box_text_get_active_text(GTK_COMBO_BOX_TEXT(view->cb_format));
}

const gchar *gydl_view_get_quality(GydlView *view)
{
        gint id;

        id = gtk_combo_box_get_active(GTK_COMBO_BOX(view->cb_quality));

        switch (id) {
        case 0:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "0" : "2160";
        case 1:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "1" : "1440";
        case 2:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "2" : "1080";
        case 3:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "3" : "720";
        case 4:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "4" : "480";
        case 5:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "5" : "360";
        case 6:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "6" : "240";
        case 7:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "7" : "144";
        case 8:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "8" : NULL;
        case 9:
                return (view->type == GYDL_VIEW_TYPE_AUDIO) ? "9" : NULL;
        default:
                return NULL;
        }
}

GydlView *gydl_view_new(GydlViewType view_type)
{
        GydlView *view;

        view = g_malloc(sizeof(GydlView));

        view->type = view_type;

        gydl_view_init(view);

        return view;
}

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
