[app]
title = Baby Wardrobe
package.name = babywardrobe
package.domain = org.vishnupriyatr27
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
requirements = python3,kivy,sqlite3,pyjnius
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.presplash = assets/splash_bg.jpg
android.icon = assets/logo.png

# OR explicitly include the folder:
android.add_assets = assets

[buildozer]
log_level = 2
