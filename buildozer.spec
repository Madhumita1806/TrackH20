[app]
title = TrackH20
package.name = trackh20
package.domain = org.madhumita

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

icon.filename = logo.png

android.permissions = INTERNET,CAMERA

android.api = 31
android.minapi = 21

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
