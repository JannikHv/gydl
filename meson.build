project('Gydl',
  version: '0.1.0'
)

py3_mod = import('python3')
i18n_mod = import('i18n')

message('Checking dependencies')
py3 = py3_mod.find_python()
gtk3 = dependency('gtk+-3.0')
pygo = dependency('pygobject-3.0')
ydl = find_program('youtube-dl')

prefix = get_option('prefix')
bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
localedir = join_paths(prefix, get_option('localedir'))

message('Getting python install path')
py3_dir = py3_mod.sysconfig_path('purelib')

message('Installing Gydl')
install_data('src/gydl.py', install_dir: bindir)

message('Installing data files')
subdir('data')
subdir('po')
