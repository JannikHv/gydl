#include "gydl-download.h"

#include <gtk/gtk.h>
#include <stdlib.h>
#include <string.h>

gboolean gydl_download_get_can_connect(const gchar *url)
{
        return g_network_monitor_can_reach(g_network_monitor_get_default(),
                                           g_network_address_new(url, 0),
                                           g_cancellable_new(),
                                           NULL);
}

gboolean gydl_download_audio(const gchar *url,
                             const gchar *format,
                             const gchar *quality)
{
        gchar *command;
        const gchar *dl_dir;
        gint len;
        gboolean exit_status;

        dl_dir = g_get_user_special_dir(G_USER_DIRECTORY_DOWNLOAD);

        len = 88;
        len += strlen(url);
        len += strlen(format);
        len += strlen(quality);
        len += strlen(dl_dir);

        command = g_malloc(sizeof(gchar) * len);

        strcpy(command, "youtube-dl --no-playlist -x --audio-format ");
        strcat(command, format);
        strcat(command, " --audio-quality ");
        strcat(command, quality);
        strcat(command, " -o \"");
        strcat(command, dl_dir);
        strcat(command, "/%(title)s.%(ext)s\" \"");
        strcat(command, url);
        strcat(command, "\"");

        exit_status = (system(command) == 0) ? TRUE : FALSE;

        g_free(command);

        return exit_status;
}

gboolean gydl_download_video(const gchar *url,
                             const gchar *format,
                             const gchar *quality)
{
        gchar *command;
        const gchar *dl_dir;
        gint len;
        gboolean exit_status;

        dl_dir = g_get_user_special_dir(G_USER_DIRECTORY_DOWNLOAD);

        len = 80;
        len += strlen(url);
        len += strlen(format);
        len += strlen(quality);
        len += strlen(dl_dir);

        command = g_malloc(sizeof(gchar) * len);

        strcpy(command, "youtube-dl --no-playlist -f [ext=");
        strcat(command, format);
        strcat(command, "+height=");
        strcat(command, quality);
        strcat(command, "] -o \"");
        strcat(command, dl_dir);
        strcat(command, "/%(title)s.%(ext)s\" \"");
        strcat(command, url);
        strcat(command, "\"");

        exit_status = (system(command) == 0) ? TRUE : FALSE;

        g_free(command);

        return exit_status;
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
