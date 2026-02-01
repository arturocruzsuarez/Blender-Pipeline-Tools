# Studio Data Normalizer v1.6 (Blender)

**Studio Data Normalizer** is a production-grade asset publishing tool designed for VFX and Animation pipelines. It automates the tedious process of cleaning, renaming, and technical normalization of 3D assets before they move down the production stream (Rigging, Layout, or Lighting).

## 🛠 Features

* **Smart Batch Renaming:** Context-aware renaming with prefix and suffix support.
* **Production Sanitization:** Automatically replaces spaces with underscores to ensure compatibility with Linux-based render farms and pipeline database standards.
* **Technical Normalization:**
    * **Freeze Transforms:** Resets Location, Rotation, and Scale (1.0) to prevent simulation and rigging artifacts.
    * **Pivot Realignment:** Quickly centers the object's origin to its geometry bounds.
    * **Material Purge:** Cleans orphan material slots to optimize file weight and scene cleanliness.
* **Professional UI:** Built with **PySide6**, featuring a "Stay on Top" hint for seamless integration within the Blender workspace.

## 🚀 Technical Highlights

This tool was developed to handle complex DCC (Digital Content Creation) integration challenges, including:

* **Context Overriding:** Implements `bpy.context.temp_override` to execute Blender operators from external UI threads, bypassing standard context restrictions in Blender 4.x.
* **Environment Injection:** Handles dynamic `sys.path` manipulation to inject PySide6 dependencies into Blender’s embedded Python interpreter.
* **Undo System Integration:** Uses `undo_push` logic to ensure all batch operations are reversible, maintaining non-destructive workflows for artists.

## 📦 Installation

To use this tool, you must install **PySide6** in your Blender Python environment.

1.  Open your terminal (as Administrator on Windows).
2.  Navigate to your Blender Python binary directory and run:
    ```powershell
    ./python.exe -m pip install PySide6
    ```
3.  Copy the script into Blender's **Text Editor**.
4.  Run the script and the UI will appear as a standalone floating window.

## 📂 Project Structure

* `studio_normalizer.py`: Main tool logic and PySide6 UI implementation.
* `README.md`: Documentation and technical overview.

---
*Developed by Arturo Cruz Suárez - Pipeline TD Candidate*
