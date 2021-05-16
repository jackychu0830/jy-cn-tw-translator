rm -Rf build dist
pyinstaller --onefile --windowed --noconfirm --clean -i jycntw.icns src/JyCnTwTranslatorApp.py
cd dist
zip  -r JyCnTwTranslatorApp.zip JyCnTwTranslatorApp.app