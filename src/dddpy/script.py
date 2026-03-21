import os
import shutil
import re
from pathlib import Path


def procesar_ruta(base_path, new_mod, new_gen, old_mod, old_gen):
    base_path = Path(base_path).resolve()
    template_path = base_path / old_mod
    target_path = base_path / new_mod

    if not template_path.exists():
        print(f"⚠️  Saltando: No existe '{old_mod}' en {base_path}")
        return

    if target_path.exists():
        # Borrado preventivo
        shutil.rmtree(target_path, ignore_errors=True)

    shutil.copytree(template_path, target_path)

    # Variantes para reemplazo inteligente
    old_gen_cap, old_gen_low = old_gen.capitalize(), old_gen.lower()
    new_gen_cap, new_gen_low = new_gen.capitalize(), new_gen.lower()
    old_mod_low, new_mod_low = old_mod.lower(), new_mod.lower()

    garbage = {".pyc", ".pyo", ".identifier", ".DS_Store"}
    ignore_dirs = {"__pycache__", ".git"}

    for root, dirs, files in os.walk(target_path, topdown=False):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for name in files:
            file_path = Path(root) / name

            # 1. Eliminar basura
            if any(name.endswith(ext) or ":Zone.Identifier" in name for ext in garbage):
                try:
                    file_path.unlink()
                except:
                    pass
                continue

            # 2. Reemplazo de contenido
            try:
                content = file_path.read_text(encoding="utf-8")
                new_content = content.replace(old_gen_cap, new_gen_cap).replace(
                    old_gen_low, new_gen_low
                )
                new_content = new_content.replace(old_mod_low, new_mod_low)
                file_path.write_text(new_content, encoding="utf-8")
            except:
                pass

            # 3. Renombrar y liberar permisos de archivo
            final_file_path = file_path
            if old_mod_low in name:
                new_name = name.replace(old_mod_low, new_mod_low)
                final_file_path = Path(root) / new_name
                file_path.rename(final_file_path)

            try:
                os.chmod(final_file_path, 0o666)
            except:
                pass

        for name in dirs:
            dir_path = Path(root) / name
            if old_mod_low in name:
                new_name = name.replace(old_mod_low, new_mod_low)
                new_dir_path = Path(root) / new_name
                dir_path.rename(new_dir_path)
                dir_path = new_dir_path

            try:
                os.chmod(dir_path, 0o777)
            except:
                pass

    try:
        os.chmod(target_path, 0o777)
    except:
        pass
    print(f"✅ Generado y permisos liberados en: {base_path}")


def generar_modulo_completo(
    new_nombre_modulo, new_nombre_general, old_nombre_modulo, old_nombre_general
):

    base_dir = Path(__file__).resolve().parent.parent

    rutas = [
        base_dir / "api",
        # base_dir / "tests",
        base_dir / "dddpy",
    ]

    print(f"🚀 Iniciando generación en Docker para '{new_nombre_modulo}'...")
    for ruta in rutas:
        procesar_ruta(
            ruta,
            new_nombre_modulo,
            new_nombre_general,
            old_nombre_modulo,
            old_nombre_general,
        )
    print("\n✨ Proceso finalizado exitosamente.")


if __name__ == "__main__":
    params = {
        "old_nombre_modulo": "brand",
        "old_nombre_general": "Brand",
        "new_nombre_modulo": "brand_manual_vector",
        "new_nombre_general": "BrandManualVector",
    }

    generar_modulo_completo(**params)
