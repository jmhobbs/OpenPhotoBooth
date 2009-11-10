## Releasing For Windows

Edit: setup.py with new version values, etc.
Run: python.exe setup.py py2exe
Copy: /etc, /lib, /share from your gtk install to /dist
Copy: LICENSE, README.markdown to /dist
Copy: static/, icons/ to /dist
Test: The executable.
Move: /dist to ../windows_installer/
Run: The NSIS script.
Test: The whole thing.