#ifndef __GYDL_DOWNLOAD_H__
#define __GYDL_DOWNLOAD_H__

#include <glib.h>

gboolean         gydl_download_get_can_connect   (const gchar *url);

gboolean         gydl_download_audio             (const gchar *url,
                                                  const gchar *format,
                                                  const gchar *quality);

gboolean         gydl_download_video             (const gchar *url,
                                                  const gchar *format,
                                                  const gchar *quality);

#endif /* __GYDL_DOWNLOAD_H__ */

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
