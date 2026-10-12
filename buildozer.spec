[app]
title = AM-MHA Pro
package.name = ammhapro
package.domain = org.ammha
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,kivy,numpy,scipy,soundfile,host_python3
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Cấu hình API và NDK tương thích ổn định nhất cho Buildozer
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.skip_update = 0
android.accept_sdk_license = True
