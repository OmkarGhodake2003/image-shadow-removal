import PyInstaller.__main__

# Path to the main Python script of your project
script_path = 'gui.py'  # Adjust if needed (this is your main script)

# PyInstaller options
PyInstaller.__main__.run([
    '--name=ShadowRemoverApp',           # Name of the output executable
    '--onefile',                         # Create a single .exe file (instead of multiple files)
    '--windowed',                        # Hide the terminal window for GUI applications
    '--add-data=Input_images;Input_images',  # Include Input_images folder
    '--add-data=Models;Models',          # Include Models folder
    '--add-data=output_images;output_images',  # Include output_images folder
    '--add-data=Samples;Samples',        # If you have additional sample data
    '--hidden-import=pkg_resources.py2_warn', # If your project has hidden imports, include them here
    script_path                          # Main Python script
])
