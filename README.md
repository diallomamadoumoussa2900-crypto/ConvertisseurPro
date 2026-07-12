name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build with Buildozer
        id: buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          workdir: .
          buildozer_version: stable
          command: buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: ConvertisseurPro-APK
          path: ${{ steps.buildozer.outputs.filename }}
