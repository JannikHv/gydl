#include "gydl-window.h"
#include "gydl-dialog.h"
#include "gydl-view.h"
#include "gydl-download.h"

#include <gtk/gtk.h>

#define GYDL_WIN_SIZE_X 525
#define GYDL_WIN_SIZE_Y 275

#define GYDL_WIN_ICON_NAME "gydl"

struct _GydlWindow {
        /* Container */
        GtkWidget *self;
        GtkWidget *hbar;
        GtkWidget *stack;

        /* Views */
        GydlView *view_audio;
        GydlView *view_video;

        /* Header bar widgets */
        GtkWidget *switcher;
        GtkWidget *btn_leave;
        GtkWidget *btn_download;
};

static void gydl_window_hide_all(GydlWindow *win)
{
        gtk_widget_hide(win->self);
        gdk_flush();
}

static void gydl_window_show_all(GydlWindow *win)
{
        gtk_widget_show_all(win->self);
        gdk_flush();
}

/**
 * "delete-event" callback function
 */
static void dialog_closed(GtkWidget *widget,
                          GydlWindow *win)
{
        gydl_window_show_all(win);
}


/**
 * "clicked" callback function
 */
static void download_button_clicked(GtkWidget *button,
                                    GydlWindow *win)
{
        GydlDialog *dialog;
        GtkWidget *window;
        const gchar *child_name;
        gboolean dl_exit;

        gydl_window_hide_all(win);

        if (!gydl_download_get_can_reach("youtube.com")) {
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_NET_ERROR);
                window = gydl_dialog_get_window(dialog);
                g_signal_connect(window,
                                 "destroy",
                                 G_CALLBACK(dialog_closed),
                                 win);
                gtk_widget_show_all(window);
                return;
        }

        child_name = gtk_stack_get_visible_child_name(GTK_STACK(win->stack));

        if (g_strcmp0(child_name, "Audio") == 0)
                dl_exit = gydl_download_get_audio(gydl_view_get_url(win->view_audio),
                                                  gydl_view_get_format(win->view_audio),
                                                  gydl_view_get_quality(win->view_audio));
        else if (g_strcmp0(child_name, "Video") == 0)
                dl_exit = gydl_download_get_video(gydl_view_get_url(win->view_video),
                                                  gydl_view_get_format(win->view_video),
                                                  gydl_view_get_quality(win->view_video));
        else
                dl_exit = FALSE;

        if (dl_exit)
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_DL_FINISH);
        else
                dialog = gydl_dialog_new(GYDL_DIALOG_TYPE_DL_ERROR);

        window = gydl_dialog_get_window(dialog);

        g_signal_connect(window,
                         "destroy",
                         G_CALLBACK(dialog_closed),
                         win);

        gtk_widget_show_all(window);
}

static void gydl_window_init(GydlWindow *win)
{
        win->self  = gtk_window_new(GTK_WINDOW_TOPLEVEL);
        win->hbar  = gtk_header_bar_new();
        win->stack = gtk_stack_new();

        win->view_audio = gydl_view_new(GYDL_VIEW_TYPE_AUDIO);
        win->view_video = gydl_view_new(GYDL_VIEW_TYPE_VIDEO);

        win->switcher     = gtk_stack_switcher_new();
        win->btn_leave    = gtk_button_new_with_label("Leave");
        win->btn_download = gtk_button_new_with_label("Download");

        /* Window */
        gtk_window_set_default_size(GTK_WINDOW(win->self),
                                    GYDL_WIN_SIZE_X,
                                    GYDL_WIN_SIZE_Y);
        gtk_window_set_titlebar(GTK_WINDOW(win->self), win->hbar);
        gtk_window_set_position(GTK_WINDOW(win->self), GTK_WIN_POS_CENTER);
        gtk_window_set_icon_name(GTK_WINDOW(win->self), GYDL_WIN_ICON_NAME);
        gtk_container_add(GTK_CONTAINER(win->self), win->stack);
        g_signal_connect(win->self,
                         "delete-event",
                         G_CALLBACK(gtk_main_quit),
                         NULL);

        /* Header bar */
        gtk_header_bar_pack_start(GTK_HEADER_BAR(win->hbar), win->btn_leave);
        gtk_header_bar_pack_end(GTK_HEADER_BAR(win->hbar), win->btn_download);
        gtk_header_bar_set_custom_title(GTK_HEADER_BAR(win->hbar), win->switcher);

        /* Stack */
        gtk_stack_set_transition_type(GTK_STACK(win->stack),
                                      GTK_STACK_TRANSITION_TYPE_SLIDE_LEFT_RIGHT);
        gtk_stack_add_titled(GTK_STACK(win->stack),
                             gydl_view_get_viewport(win->view_audio),
                             "Audio",
                             "Audio");
        gtk_stack_add_titled(GTK_STACK(win->stack),
                             gydl_view_get_viewport(win->view_video),
                             "Video",
                             "Video");

        /* Stack switcher */
        gtk_stack_switcher_set_stack(GTK_STACK_SWITCHER(win->switcher),
                                     GTK_STACK(win->stack));

        /* Header bar buttons */
        g_signal_connect(win->btn_leave,
                         "clicked",
                         G_CALLBACK(gtk_main_quit),
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

GtkWidget *gydl_window_new(void)
{
        GydlWindow *win;

        win = g_malloc(sizeof(GydlWindow));

        gydl_window_init(win);

        return win->self;
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
