i18n_mod.merge_file(
  input: 'com.github.JannikHv.Gydl.appdata.xml.in',
  output: 'com.github.JannikHv.Gydl.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(datadir, 'metainfo')
)

i18n_mod.merge_file(
  input: 'com.github.JannikHv.Gydl.desktop.in',
  output: 'com.github.JannikHv.Gydl.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(datadir, 'applications')
)

icondir = join_paths(datadir, 'icons/hicolor')
install_data(
  'gydl.svg',
  install_dir: join_paths(icondir, 'scalable/apps')
)
