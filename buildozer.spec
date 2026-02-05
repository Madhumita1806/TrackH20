[app]

# (str) Title of your application
title = TrackH2O

# (str) Package name
package.name = trackh2o

# (str) Package domain (important)
package.domain = org.madhumita

# (str) Source code directory
source.dir = .

# (str) The main .py file
source.main = main.py

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0


# -------------------------
# Versioning
# -------------------------

# (str) Application version
version = 0.1

# (int) Android version code
android.numeric_version = 1


# -------------------------
# Android Configuration
# -------------------------

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to build with
android.api = 31

# (int) Minimum Android API
android.minapi = 21

# (list) Architectures
android.archs = arm64-v8a

# (str) Bootstrap
android.bootstrap = sdl2

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Copy libs instead of symlinking
android.copy_libs = 1


# -------------------------
# Build Options
# -------------------------

# (bool) Log level
log_level = 2

# (bool) Enable debug build
android.debug = True

# (bool) Ignore setup.py
android.ignore_setup_py = True


# -------------------------
# Packaging
# -------------------------

# (bool) Include python files
include_exts = py,png,jpg,kv

# (str) Presplash color
presplash_color = #FFFFFF

# (str) Icon (optional)
# icon.filename = %(source.dir)s/icon.png


# -------------------------
# Python & Buildozer
# -------------------------

[buildozer]

# (int) Buildozer API version
api = 31

# (str) Path to buildozer directory
build_dir = .buildozer
