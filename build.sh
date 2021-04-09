rm -Rf build dist
pyinstaller --onefile --windowed --noconfirm --clean -c -F -i jycntw.icns src/JyCnTwTranslatorApp.py
cd dist
zip  JyCnTwTranslatorApp.zip JyCnTwTranslatorApp