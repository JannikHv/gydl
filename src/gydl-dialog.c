#include "gydl-dialog.h"

#include <gtk/gtk.h>

#define GYDL_DIALOG_SIZE_X 400
#define GYDL_DIALOG_SIZE_Y 200

#define GYDL_DIALOG_ICON_NAME "gydl"

struct _GydlDialog {
        /* Containers */
        GtkWidget *self;
        GtkWidget *hbar;
        GtkWidget *grid;

        /* Widgets */
        GtkWidget *label;
        GtkWidget *btn_leave;
        GtkWidget *btn_continue;

        /* Type */
        GydlDialogType type;
};

/**
 * "clicked" callback function
 */
static void continue_button_clicked(GtkWidget *button,
                                    GydlDialog *dialog)
{
        g_signal_handlers_disconnect_by_func(dialog->self,
                                             gtk_main_quit,
                                             NULL);
        gtk_window_close(GTK_WINDOW(dialog->self));
}

static const gchar *get_title_from_type(GydlDialogType dialog_type)
{
        switch (dialog_type) {
        case GYDL_DIALOG_TYPE_NET_ERROR:
             return "Connection Error";
        case GYDL_DIALOG_TYPE_DL_ERROR:
             return "Download Failed";
        case GYDL_DIALOG_TYPE_DL_FINISH:
             return "Download Successful";
        default:
             return NULL;
        }
}

static const gchar *get_text_from_type(GydlDialogType dialog_type)
{
        switch (dialog_type) {
        case GYDL_DIALOG_TYPE_NET_ERROR:
             return "An internet connection error has occured.\n"\
                    "Make sure you're connected to the internet.";
        case GYDL_DIALOG_TYPE_DL_ERROR:
             return "The download has been unsuccessful.\n"\
                    "Make sure the URL you've entered is valid.";
        case GYDL_DIALOG_TYPE_DL_FINISH:
             return "The download has been successful.\n"\
                    "The file has been saved in your download folder.";
        default:
             return NULL;
        }
}

static void gydl_dialog_init(GydlDialog *dialog)
{
        dialog->self = gtk_window_new(GTK_WINDOW_TOPLEVEL);
        dialog->hbar = gtk_header_bar_new();
        dialog->grid = gtk_grid_new();

        dialog->label = gtk_label_new(NULL);
        dialog->btn_leave = gtk_button_new_with_label("Leave");
        dialog->btn_continue = gtk_button_new_with_label("Continue");

        /* Window */
        gtk_window_set_default_size(GTK_WINDOW(dialog->self),
                                    GYDL_DIALOG_SIZE_X,
                                    GYDL_DIALOG_SIZE_Y);
        gtk_window_set_titlebar(GTK_WINDOW(dialog->self), dialog->hbar);
        gtk_window_set_position(GTK_WINDOW(dialog->self), GTK_WIN_POS_CENTER);
        gtk_window_set_icon_name(GTK_WINDOW(dialog->self), GYDL_DIALOG_ICON_NAME);
        gtk_container_add(GTK_CONTAINER(dialog->self), dialog->grid);
        g_signal_connect(dialog->self,
                         "delete-event",
                         gtk_main_quit,
                         NULL);

        /* Header bar */
        gtk_header_bar_set_title(GTK_HEADER_BAR(dialog->hbar),
                                 get_title_from_type(dialog->type));

        /* Grid */
        gtk_grid_set_column_homogeneous(GTK_GRID(dialog->grid), TRUE);
        gtk_grid_set_row_homogeneous(GTK_GRID(dialog->grid), TRUE);

        /* Label */
        gtk_label_set_text(GTK_LABEL(dialog->label),
                           get_text_from_type(dialog->type));

        /* Buttons */
        g_signal_connect(dialog->btn_leave,
                         "clicked",
                         G_CALLBACK(gtk_main_quit),
                         NULL);
        g_signal_connect(dialog->btn_continue,
                         "clicked",
                         G_CALLBACK(continue_button_clicked),
                         dialog);
        gtk_style_context_add_class(gtk_widget_get_style_context(dialog->btn_continue),
                                    "suggested-action");

        /* Attach widgets to grid */
        gtk_grid_attach(GTK_GRID(dialog->grid),
                        dialog->label,
                        0, 0, 2, 3);
        gtk_grid_attach(GTK_GRID(dialog->grid),
                        dialog->btn_leave,
                        0, 3, 1, 1);
        gtk_grid_attach(GTK_GRID(dialog->grid),
                        dialog->btn_continue,
                        1, 3, 1, 1);
}

/**
 * Accessors
 */
GtkWidget *gydl_dialog_get_window(GydlDialog *dialog)
{
        return dialog->self;
}

GydlDialog *gydl_dialog_new(GydlDialogType dialog_type)
{
        GydlDialog *dialog;

        dialog = g_malloc(sizeof(GydlDialog));

        dialog->type = dialog_type;

        gydl_dialog_init(dialog);

        return dialog;
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
