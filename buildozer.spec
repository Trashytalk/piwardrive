[app]
# (str) Title of your application
title = PiWardrive

# (str) Package name
package.name = piwardrive

# (str) Package domain (needed for android/ios packaging)
package.domain = org.piwardrive

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
requirements = python3,kivy,kivymd,kivy_garden.mapview,kivy_garden.graph,requests,requests-cache,psutil,scipy,pydantic,ujson,PyYAML,matplotlib,cryptography,fastapi,uvicorn,httpx

# (str) Application version
version = 0.1

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1
