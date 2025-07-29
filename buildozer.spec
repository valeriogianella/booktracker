# Buildozer configuration for Android APK
[app]
title = BookTrack
package.name = booktrack
package.domain = com.booktrack

source.dir = src
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0
requirements = python3,kivy,kivymd

[buildozer]
log_level = 2

[app]
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
warn_on_root = 1
