copy src\JyCnTwTranslatorApp.py src\JyCnTwTranslatorWinApp.py
pyinstaller -c -F -y --win-private-assemblies --win-no-prefer-redirects -i icon.ico src\JyCnTwTranslatorWinApp.py