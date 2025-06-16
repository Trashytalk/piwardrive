Mobile Builds
=============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


This guide explains how to package PiWardrive for Android and iOS.

Prerequisites
-------------

* **Android**: Python 3.10 or later, Java JDK 17, Android SDK/NDK and
  ``buildozer`` (``pip install buildozer``).
* **iOS**: macOS with Xcode installed and ``kivy-ios``
  (``pip install kivy-ios sh pbxproj cookiecutter``).

Android
-------

Use the helper script to build the debug APK::

    ./scripts/build_android.sh

The first run downloads the Android toolchain and may take time. The
APK is placed under ``bin/``. Adjust ``buildozer.spec`` to change the
package name or permissions.

iOS
---

To generate an Xcode project run::

    ./scripts/build_ios.sh

Open the created project in Xcode to build and sign the app.

Mobile-specific Adjustments
---------------------------

System service management and some diagnostics rely on Linux-only
utilities. When running on Android or iOS those features are disabled.
Check ``kivy.utils.platform`` at runtime to detect the platform.
