rm -Rf build dist
pyinstaller --onefile --windowed --noconfirm --clean -i jycntw.icns src/JyCnTwTranslatorApp.py
cd dist
zip  JyCnTwTranslatorApp.zip JyCnTwTranslatorApp