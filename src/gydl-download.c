#include "gydl-download.h"

#include <gtk/gtk.h>
#include <string.h>
#include <stdlib.h>

gboolean gydl_download_get_can_reach(const gchar *url)
{
        return g_network_monitor_can_reach(g_network_monitor_get_default(),
                                           g_network_address_new(url, 0),
                                           g_cancellable_new(),
                                           NULL);
}

gboolean gydl_download_get_audio(const gchar *url,
                                 const gchar *format,
                                 const gchar *quality)
{
        gint len;
        gchar *cmd;
        const gchar *dl_dir;

        dl_dir = g_get_user_special_dir(G_USER_DIRECTORY_DOWNLOAD);

        len = 88;
        len += strlen(url);
        len += strlen(format);
        len += strlen(quality);
        len += strlen(dl_dir);

        cmd = g_malloc(sizeof(gchar) * len);

        strcpy(cmd, "youtube-dl --no-playlist -x --audio-format ");
        strcat(cmd, format);
        strcat(cmd, " --audio-quality ");
        strcat(cmd, quality);
        strcat(cmd, " -o \"");
        strcat(cmd, dl_dir);
        strcat(cmd, "/%(title)s.%(ext)s\" \"");
        strcat(cmd, url);
        strcat(cmd, "\"");

        printf("%s\n", cmd);

        return (system(cmd) == 0) ? TRUE : FALSE;
}

gboolean gydl_download_get_video(const gchar *url,
                                 const gchar *format,
                                 const gchar *quality)
{
        gint len;
        gchar *cmd;
        const gchar *dl_dir;

        dl_dir = g_get_user_special_dir(G_USER_DIRECTORY_DOWNLOAD);

        len = 71;
        len += strlen(url);
        len += strlen(format);
        len += strlen(quality);
        len += strlen(dl_dir);

        cmd = g_malloc(sizeof(gchar) * len);

        strcpy(cmd, "youtube-dl --no-playlist -f [ext=");
        strcat(cmd, format);
        strcat(cmd, "+height=");
        strcat(cmd, quality);
        strcat(cmd, "] -o \"");
        strcat(cmd, dl_dir);
        strcat(cmd, "/%(title)s.%(ext)s\" \"");
        strcat(cmd, url);
        strcat(cmd, "\"");

        printf("%s\n", cmd);

        return (system(cmd) == 0) ? TRUE : FALSE;
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
