# Orca Post-Processing – Command and Notes

**Command (Linux):**
python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

**Command (Windows):**
python "C:\Users<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

**Notes**
- The script waits ~1.5 s to ensure the G-code is fully written.
- If no G-code is present in the watched folder, it returns “No gcode file found”.
- Output name is derived from the header line `; printing object ...` (base name, no extension).
- Thumbnails are optional but recommended; put them in the same folder as the script.
