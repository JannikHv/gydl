#include "gydl-view.h"

#include <gtk/gtk.h>
#include <string.h>

struct _GydlView {
        /* Container */
        GtkWidget *grid;

        /* Labels */
        GtkWidget *l_url;
        GtkWidget *l_format;
        GtkWidget *l_quality;

        /* Widgets */
        GtkWidget *entry;
        GtkWidget *cb_format;
        GtkWidget *cb_quality;
};

static const gchar *get_markup_from_text(const gchar *text)
{
        gint len;
        gchar *markup;

        len = strlen(text);
        len += 36;

        markup = g_malloc(sizeof(gchar) * len);

        strcpy(markup, "<span size='15000'><u>\n");
        strcat(markup, text);
        strcat(markup, "\n</u></span>");

        return markup;
}

static void gydl_view_audio_init(GydlView *view)
{
        GtkComboBoxText *cb_format, *cb_quality;
        gint i;

        const gchar *format[5] = {
                "aac", "m4a", "mp3", "ogg", "wav"
        };

        const gchar *quality[10] = {
                "0", "1", "2", "3", "4",
                "5", "6", "7", "8", "9",
        };

        cb_format = GTK_COMBO_BOX_TEXT(view->cb_format);
        cb_quality = GTK_COMBO_BOX_TEXT(view->cb_quality);

        for (i = 0; i < 5; i++)
                gtk_combo_box_text_append_text(cb_format, format[i]);

        for (i = 0; i < 10; i++)
                gtk_combo_box_text_append_text(cb_quality, quality[i]);

        gtk_combo_box_set_active(GTK_COMBO_BOX(cb_format), 2);
        gtk_combo_box_set_active(GTK_COMBO_BOX(cb_quality), 5);
}

static void gydl_view_video_init(GydlView *view)
{
        GtkComboBoxText *cb_format, *cb_quality;
        gint i;

        const gchar *format[4] = {
                "3gp", "flv", "mp4", "webm",
        };

        const gchar *quality[8] = {
                "2160p", "1440p", "1080p", "720p",
                "480p", "360p", "240p", "144p",
        };

        cb_format = GTK_COMBO_BOX_TEXT(view->cb_format);
        cb_quality = GTK_COMBO_BOX_TEXT(view->cb_quality);

        for (i = 0; i < 4; i++)
                gtk_combo_box_text_append_text(cb_format, format[i]);

        for (i = 0; i < 8; i++)
                gtk_combo_box_text_append_text(cb_quality, quality[i]);

        gtk_combo_box_set_active(GTK_COMBO_BOX(cb_format), 2);
        gtk_combo_box_set_active(GTK_COMBO_BOX(cb_quality), 3);
}

static void gydl_view_add_interface(GydlView *view)
{
        GtkGrid *grid;

        grid = GTK_GRID(view->grid);

        gtk_grid_attach(grid, view->l_url, 0, 0, 4, 1);
        gtk_grid_attach(grid, view->entry, 0, 1, 4, 1);
        gtk_grid_attach(grid, view->l_format, 0, 2, 2, 1);
        gtk_grid_attach(grid, view->l_quality, 2, 2, 2, 1);
        gtk_grid_attach(grid, view->cb_format, 0, 3, 2, 1);
        gtk_grid_attach(grid, view->cb_quality, 2, 3, 2, 1);
}

static void gydl_view_init(GydlView *view,
                           GydlViewType type)
{
        view->grid = gtk_grid_new();

        view->l_url     = gtk_label_new(NULL);
        view->l_format  = gtk_label_new(NULL);
        view->l_quality = gtk_label_new(NULL);

        view->entry      = gtk_entry_new();
        view->cb_format  = gtk_combo_box_text_new();
        view->cb_quality = gtk_combo_box_text_new();

        /* Grid */
        gtk_grid_set_column_homogeneous(GTK_GRID(view->grid), TRUE);
        gtk_container_set_border_width(GTK_CONTAINER(view->grid), 10);

        /* Labels */
        gtk_label_set_markup(GTK_LABEL(view->l_url),
                             get_markup_from_text("Enter the URL"));
        gtk_label_set_markup(GTK_LABEL(view->l_format),
                             get_markup_from_text("Format"));
        gtk_label_set_markup(GTK_LABEL(view->l_quality),
                             get_markup_from_text("Quality"));

        /* Entry */
        gtk_entry_set_placeholder_text(GTK_ENTRY(view->entry),
                                       "https://youtube.com/watch...");

        /* Combo boxes */
        gtk_container_set_border_width(GTK_CONTAINER(view->cb_format), 5);
        gtk_container_set_border_width(GTK_CONTAINER(view->cb_quality), 5);

        switch (type) {
        case GYDL_VIEW_TYPE_AUDIO:
                gydl_view_audio_init(view);
                break;
        case GYDL_VIEW_TYPE_VIDEO:
                gydl_view_video_init(view);
                break;
        default:
                break;
        }

        gydl_view_add_interface(view);
}

/**
 * Accessors
 */
GtkWidget *gydl_view_get_viewport(GydlView *view)
{
        return view->grid;
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
        return gtk_combo_box_text_get_active_text(GTK_COMBO_BOX_TEXT(view->cb_quality));
}

GydlView *gydl_view_new(GydlViewType type)
{
        GydlView *view;

        view = g_malloc(sizeof(GydlView));

        gydl_view_init(view, type);

        return view;
}
