import sys
import os
import bpy

# --- CONFIGURACIÓN DE ENTORNO ---
site_path = os.path.join(sys.prefix, "lib", "site-packages")
if site_path not in sys.path:
    sys.path.append(site_path)

pyside_bin_path = os.path.join(site_path, "PySide6")
if os.path.exists(pyside_bin_path):
    os.environ["PATH"] += os.pathsep + pyside_bin_path

try:
    from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFrame,
                                 QLineEdit, QPushButton, QLabel, QGridLayout, QMessageBox)
    from PySide6.QtCore import Qt
except ImportError:
    print("ERROR: No se encontraron las dependencias de PySide6.")

class StudioDataNormalizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studio Data Normalizer | Professional Suite")
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- SECCIÓN 1: NAMING CONVENTION ---
        layout.addWidget(QLabel("<b>1. CONVENCIÓN DE NOMENCLATURA</b>"))
        grid = QGridLayout()
        grid.addWidget(QLabel("Prefijo:"), 0, 0)
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("ej. CHR_")
        grid.addWidget(self.prefix_input, 0, 1)
        
        grid.addWidget(QLabel("Sufijo:"), 1, 0)
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("ej. _LOD0")
        grid.addWidget(self.suffix_input, 1, 1)
        layout.addLayout(grid)
        
        self.rename_btn = QPushButton("EJECUTAR RENOMBRADO BATCH")
        self.rename_btn.setStyleSheet("background-color: #2b5b2d; color: white; font-weight: bold; height: 30px;")
        self.rename_btn.clicked.connect(self.run_rename)
        layout.addWidget(self.rename_btn)

        line = QFrame(); line.setFrameShape(QFrame.HLine); layout.addWidget(line)

        # --- SECCIÓN 2: NORMALIZACIÓN TÉCNICA ---
        layout.addWidget(QLabel("<b>2. PUBLICACIÓN DE ASSETS (NORMALIZACIÓN)</b>"))
        
        self.freeze_btn = QPushButton("CONGELAR TRANSFORMACIONES (Loc/Rot/Scale)")
        self.freeze_btn.clicked.connect(self.freeze_transforms)
        layout.addWidget(self.freeze_btn)
        
        self.pivot_btn = QPushButton("CENTRAR PIVOTE A GEOMETRÍA")
        self.pivot_btn.clicked.connect(self.center_pivot)
        layout.addWidget(self.pivot_btn)

        self.clean_mat_btn = QPushButton("LIMPIAR SLOTS DE MATERIALES")
        self.clean_mat_btn.clicked.connect(self.clean_materials)
        layout.addWidget(self.clean_mat_btn)

    def get_selected(self):
        """Obtiene objetos seleccionados de forma segura."""
        try:
            return bpy.context.view_layer.objects.selected
        except:
            return [obj for obj in bpy.context.selectable_objects if obj.select_get()]

    def run_rename(self):
        prefix = self.prefix_input.text().strip()
        suffix = self.suffix_input.text().strip()
        objetos = self.get_selected()
        
        if not objetos: 
            QMessageBox.warning(self, "Error", "No hay objetos seleccionados.")
            return
        
        # SOLUCIÓN AL ERROR: Aplicar override al Undo
        try:
            with bpy.context.temp_override(window=bpy.context.window):
                bpy.ops.ed.undo_push(message="Smart Rename")
        except: pass

        for obj in objetos:
            new_name = obj.name
            if prefix and not new_name.startswith(prefix):
                new_name = f"{prefix}{new_name}"
            if suffix and not new_name.endswith(suffix):
                new_name = f"{new_name}{suffix}"
            obj.name = new_name.replace(" ", "_")

    def freeze_transforms(self):
        objetos = self.get_selected()
        if not objetos: return
        
        try:
            with bpy.context.temp_override(window=bpy.context.window):
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            QMessageBox.information(self, "Éxito", "Transformaciones congeladas (1.0 Scale).")
        except Exception as e:
            print(f"Error en Freeze: {e}")

    def center_pivot(self):
        objetos = self.get_selected()
        if not objetos: return
        try:
            with bpy.context.temp_override(window=bpy.context.window):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            QMessageBox.information(self, "Éxito", "Pivotes centrados.")
        except Exception as e:
            print(f"Error en Pivot: {e}")

    def clean_materials(self):
        objetos = self.get_selected()
        for obj in objetos:
            if obj.type == 'MESH':
                obj.data.materials.clear()
        QMessageBox.information(self, "Éxito", "Materiales eliminados.")

if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    window = StudioDataNormalizer()
    window.show()