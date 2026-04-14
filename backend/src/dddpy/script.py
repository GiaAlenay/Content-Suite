import os
import shutil
from pathlib import Path


def procesar_ruta(base_path, new_mod, new_gen, old_mod, old_gen):
    base_path = Path(base_path).resolve()
    template_path = base_path / old_mod
    target_path = base_path / new_mod

    if not template_path.exists():
        print(f"⚠️  Saltando: No existe '{old_mod}' en {base_path}")
        return

    if target_path.exists():
        shutil.rmtree(target_path, ignore_errors=True)

    shutil.copytree(template_path, target_path)

    # Definimos los pares de reemplazo (de lo más específico a lo más general)
    reemplazos = [
        (old_gen, new_gen),  # ManualRecord -> ManualVersion
        (old_gen.lower(), new_gen.lower()),  # manualrecord -> manualversion
        (old_mod, new_mod),  # manual_record -> manual_version
    ]

    garbage = {".pyc", ".pyo", ".identifier", ".DS_Store"}
    ignore_dirs = {"__pycache__", ".git"}

    for root, dirs, files in os.walk(target_path, topdown=False):
        # Filtrar directorios a ignorar
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

            # 2. Reemplazo de contenido (Optimizado)
            try:
                content = file_path.read_text(encoding="utf-8")
                new_content = content
                for old_val, new_val in reemplazos:
                    new_content = new_content.replace(old_val, new_val)

                file_path.write_text(new_content, encoding="utf-8")
            except Exception as e:
                print(f"❌ Error leyendo archivo {name}: {e}")

            # 3. Renombrar archivo
            new_name = name
            for old_val, new_val in reemplazos:
                new_name = new_name.replace(old_val, new_val)

            final_file_path = file_path
            if new_name != name:
                final_file_path = Path(root) / new_name
                file_path.rename(final_file_path)

            try:
                os.chmod(final_file_path, 0o666)
            except:
                pass

        # 4. Renombrar directorios
        for name in dirs:
            dir_path = Path(root) / name
            new_dir_name = name
            for old_val, new_val in reemplazos:
                new_dir_name = new_dir_name.replace(old_val, new_val)

            if new_dir_name != name:
                new_dir_path = Path(root) / new_dir_name
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
    print(f"✅ Procesado: {target_path}")


def generar_modulo_completo(
    new_nombre_modulo, new_nombre_general, old_nombre_modulo, old_nombre_general
):

    base_dir = Path(__file__).resolve().parent.parent

    rutas = [base_dir / "api", base_dir / "dddpy"]

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
        "old_nombre_modulo": "manual_section",
        "old_nombre_general": "ManualSection",
        "new_nombre_modulo": "chat_history",
        "new_nombre_general": "ChatHistory",
    }

    generar_modulo_completo(**params)
