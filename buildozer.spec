[app]

# (string) Title of your application
title = Randoms Discord ToolKit

# (string) Package name
package.name = RandomsToolkit

# (string) Package domain (needed for android packaging)
package.domain = org.randomcore

# (string) Source code directory
source.dir = .

# (list) Source files to include (leave empty to include everything)
source.include_exts = py,png,jpg,kv,atlas

# (string) Application versioning
version = 2.0

# (list) Application requirements
# CRITICAL: Ensures requests and all its SSL parsing network dependencies are included
requirements = python3, kivy, requests, charset-normalizer, idna, urllib3, certifi

# (str) Supported orientations
orientation = portrait

#
# Android specific settings
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) System permissions to allow network transmissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Automatically accept SDK license agreements for automation platforms
android.accept_sdk_license = True

# (str) The Android architectural target
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
