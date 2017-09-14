#include "gydl-window.h"
#include "gydl-view.h"
#include "gydl-dialog.h"
#include "gydl-download.h"

#include <gtk/gtk.h>

#define GYDL_WIN_SIZE_X 525
#define GYDL_WIN_SIZE_Y 275

#define GYDL_STACK_NAME_AUDIO "gydl-audio-stack"
#define GYDL_STACK_NAME_VIDEO "gydl-video-stack"

struct _GydlWindow {
        /* Containers */
        GtkWidget *self;
        GtkWidget *hbar;
        GtkWidget *stack;
        GtkWidget *switcher;

        /* Views */
        GydlView *view_audio;
        GydlView *view_video;

        /* Header bar widgets */
        GtkWidget *btn_cancel;
        GtkWidget *btn_download;
};

static void gydl_window_hide(GydlWindow *win)
{
        gtk_widget_hide(win->self);
        gdk_flush();
}

static void download_button_clicked(GtkWidget *button,
                                    GydlWindow *win)
{
        GydlDialog *dialog;
        GtkWidget *dialog_win;
        const gchar *visible_child;
        gboolean dl_status;

        gydl_window_hide(win);

        /* Check if internet connection is working */
        if (!gydl_download_get_can_connect("youtube.com")) {
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_NET_ERR);
                dialog_win = gydl_dialog_get_window(dialog);
                gydl_dialog_set_window(dialog, win);
                gtk_widget_show_all(dialog_win);
                return;
        }

        visible_child = gtk_stack_get_visible_child_name(GTK_STACK(win->stack));

        /* Try to download audio/video */
        if (g_strcmp0(visible_child, GYDL_STACK_NAME_AUDIO) == 0)
                dl_status = gydl_download_audio(gydl_view_get_url(win->view_audio),
                                                gydl_view_get_format(win->view_audio),
                                                gydl_view_get_quality(win->view_audio));
        else
                dl_status = gydl_download_video(gydl_view_get_url(win->view_video),
                                                gydl_view_get_format(win->view_video),
                                                gydl_view_get_quality(win->view_video));

        /* Check if download was successful */
        if (dl_status)
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_DL_SUCCESS);
        else
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_DL_FAIL);

        dialog_win = gydl_dialog_get_window(dialog);
        gydl_dialog_set_window(dialog, win);
        gtk_widget_show_all(dialog_win);
}

static void gydl_window_init(GydlWindow *win)
{
        win->self     = gtk_window_new(GTK_WINDOW_TOPLEVEL);
        win->hbar     = gtk_header_bar_new();
        win->stack    = gtk_stack_new();
        win->switcher = gtk_stack_switcher_new();

        win->view_audio = gydl_view_new(GYDL_VIEW_TYPE_AUDIO);
        win->view_video = gydl_view_new(GYDL_VIEW_TYPE_VIDEO);

        win->btn_cancel   = gtk_button_new_with_label("Cancel");
        win->btn_download = gtk_button_new_with_label("Download");

        /* Window */
        gtk_window_set_default_size(GTK_WINDOW(win->self),
                                    GYDL_WIN_SIZE_X,
                                    GYDL_WIN_SIZE_Y);
        gtk_window_set_titlebar(GTK_WINDOW(win->self), win->hbar);
        gtk_window_set_position(GTK_WINDOW(win->self), GTK_WIN_POS_CENTER);
        gtk_window_set_icon_name(GTK_WINDOW(win->self), "gydl");
        gtk_container_add(GTK_CONTAINER(win->self), win->stack);
        g_signal_connect(win->self,
                         "delete-event",
                         gtk_main_quit,
                         NULL);

        /* Header bar */
        gtk_header_bar_pack_start(GTK_HEADER_BAR(win->hbar), win->btn_cancel);
        gtk_header_bar_pack_end(GTK_HEADER_BAR(win->hbar), win->btn_download);
        gtk_header_bar_set_custom_title(GTK_HEADER_BAR(win->hbar), win->switcher);

        /* Stack */
        gtk_stack_set_transition_type(GTK_STACK(win->stack),
                                      GTK_STACK_TRANSITION_TYPE_SLIDE_LEFT_RIGHT);
        gtk_stack_add_titled(GTK_STACK(win->stack),
                             gydl_view_get_viewport(win->view_audio),
                             GYDL_STACK_NAME_AUDIO,
                             "Audio");
        gtk_stack_add_titled(GTK_STACK(win->stack),
                             gydl_view_get_viewport(win->view_video),
                             GYDL_STACK_NAME_VIDEO,
                             "Video");

        /* Stack switcher */
        gtk_stack_switcher_set_stack(GTK_STACK_SWITCHER(win->switcher),
                                     GTK_STACK(win->stack));

        /* Header bar buttons */
        g_signal_connect(win->btn_cancel,
                         "clicked",
                         gtk_main_quit,
                         NULL);
        g_signal_connect(win->btn_download,
                         "clicked",
                         G_CALLBACK(download_button_clicked),
                         win);
        gtk_style_context_add_class(gtk_widget_get_style_context(win->btn_download),
                                    "suggested-action");
}

/**
 * Accessors
 */
void gydl_window_show_all(GydlWindow *win)
{
        gtk_widget_show_all(win->self);
        gdk_flush();
}

GydlWindow *gydl_window_new(void)
{
        GydlWindow *win;

        win = g_malloc(sizeof(GydlWindow));

        gydl_window_init(win);

        return win;
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
