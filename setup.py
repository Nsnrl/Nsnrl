import cx_Freeze
executables = [cx_Freeze.Executable("main.py",
                                    icon=r"res\convertir.ico",
                                    base="Win32GUI")]

cx_Freeze.setup(
    name = "Heilmann_Software",
    version = "0.3",
    options={
        "build_exe": {
            "include_files": ["res/"],
            "packages":["PIL", "pytesseract", "cv2"],
        }
    },
    executables = executables
)