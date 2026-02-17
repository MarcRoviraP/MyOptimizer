import json
import os
import flet as ft
from main import Configuracion

PERFIL = "config_Optimizador.json"
ACCENT = "#5B7FFF"
ACCENT_LIGHT = "#EEF1FF"

ICON_POOL = [
    ft.Icons.PHOTO_OUTLINED, ft.Icons.DRAW_OUTLINED,
    ft.Icons.PICTURE_AS_PDF_OUTLINED, ft.Icons.DESCRIPTION_OUTLINED,
    ft.Icons.TABLE_CHART_OUTLINED, ft.Icons.SLIDESHOW_OUTLINED,
    ft.Icons.TEXT_SNIPPET_OUTLINED, ft.Icons.BOOK_OUTLINED,
    ft.Icons.DATA_OBJECT, ft.Icons.APP_SETTINGS_ALT,
    ft.Icons.FOLDER_ZIP_OUTLINED, ft.Icons.VIDEO_LIBRARY_OUTLINED,
    ft.Icons.AUDIO_FILE_OUTLINED, ft.Icons.CODE,
    ft.Icons.STORAGE_OUTLINED, ft.Icons.SETTINGS_OUTLINED,
    ft.Icons.FONT_DOWNLOAD_OUTLINED, ft.Icons.ARTICLE_OUTLINED,
    ft.Icons.ACCESS_TIME, ft.Icons.LINK, ft.Icons.FOLDER_OUTLINED,
]


def main(page: ft.Page):
    nombre_perfil = PERFIL.replace("config_", "").replace(".json", "")
    page.title = f"MyOptimizer — {nombre_perfil}"
    page.bgcolor = "#FAFAFA"
    page.padding = 0
    page.scroll = None

    config = Configuracion()
    categorias_data = config.viewProfile(PERFIL)
    ruta_json = os.path.join(config.RUTA_CONFIG, PERFIL)

    # Estado: refs a widgets por categoría y estado expandir/colapsar
    cat_refs = {}        # cat_name -> {"ext_row", "badge", "tile", "input"}
    expanded = {}        # cat_name -> bool
    tree_column = ft.Column(spacing=0, scroll="auto")
    status_text = ft.Text("", size=11, color="#888888", italic=True)

    def mostrar_status(msg):
        status_text.value = msg
        status_text.update()

    def icono_para(idx):
        return ICON_POOL[idx % len(ICON_POOL)]

    # ─── Crear chip de extensión ───

    def crear_chip(ext, cat_name):
        return ft.Draggable(
            group="ext",
            data={"ext": ext, "from": cat_name},
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f".{ext}", size=11, weight=ft.FontWeight.W_500,
                                color="#444444", font_family="Consolas"),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE, icon_size=10,
                            icon_color="#CCCCCC", tooltip="Quitar",
                            on_click=lambda e, c=cat_name, x=ext: quitar_ext(
                                c, x),
                            width=20, height=20,
                        ),
                    ],
                    spacing=2, tight=True,
                ),
                bgcolor="#FFFFFF",
                padding=ft.Padding(6, 2, 2, 2),
                border_radius=4,
                border=ft.Border.all(1, "#E0E0E0"),
            ),
        )

    # ─── Actualizar solo el contenido de UNA categoría (sin rebuild) ───

    def actualizar_cat_ui(cat_name):
        """Actualiza chips y badge de una categoría SIN reconstruir el tile."""
        ref = cat_refs.get(cat_name)
        if not ref:
            return
        exts = categorias_data.get(cat_name, [])
        ext_row = ref["ext_row"]

        # Reconstruir chips
        ext_row.controls.clear()
        if exts:
            for e in sorted(exts):
                ext_row.controls.append(crear_chip(e, cat_name))
        else:
            ext_row.controls.append(
                ft.Text("sin extensiones", size=11,
                        italic=True, color="#CCCCCC")
            )
        ext_row.update()

        # Actualizar badge
        ref["badge"].value = str(len(exts))
        ref["badge"].update()

    # ─── Acciones ───

    def agregar_ext(cat_name, valor, input_ctrl):
        ext = valor.strip().lower().lstrip(".")
        if not ext:
            return
        if ext in categorias_data[cat_name]:
            mostrar_status(
                f"⚠ .{ext} ya existe en {cat_name.replace('_', ' ')}")
            return
        categorias_data[cat_name].append(ext)
        input_ctrl.value = ""
        input_ctrl.update()
        actualizar_cat_ui(cat_name)
        mostrar_status(f"+ .{ext} → {cat_name.replace('_', ' ')}")

    def quitar_ext(cat_name, ext):
        if ext in categorias_data[cat_name]:
            categorias_data[cat_name].remove(ext)
        actualizar_cat_ui(cat_name)
        mostrar_status(f"− .{ext} de {cat_name.replace('_', ' ')}")

    def on_drop(e, cat_destino):
        src = page.get_control(e.src_id)
        data = src.data
        if isinstance(data, str):
            data = json.loads(data)
        ext = data["ext"]
        cat_origen = data["from"]
        if cat_origen == cat_destino:
            return
        if ext in categorias_data[cat_origen]:
            categorias_data[cat_origen].remove(ext)
        if ext not in categorias_data[cat_destino]:
            categorias_data[cat_destino].append(ext)
        actualizar_cat_ui(cat_origen)
        actualizar_cat_ui(cat_destino)
        mostrar_status(
            f".{ext}  {cat_origen.replace('_', ' ')} → {cat_destino.replace('_', ' ')}")

    def eliminar_cat(cat_name):
        if cat_name in categorias_data:
            del categorias_data[cat_name]
        if cat_name in cat_refs:
            del cat_refs[cat_name]
        if cat_name in expanded:
            del expanded[cat_name]
        rebuild_tree()
        mostrar_status(f"✕ {cat_name.replace('_', ' ')} eliminada")

    def crear_categoria(e):
        nombre = new_cat_input.value.strip()
        if not nombre:
            return
        key = nombre.replace(" ", "_")
        if key in categorias_data:
            mostrar_status(f"⚠ '{nombre}' ya existe")
            return
        categorias_data[key] = []
        expanded[key] = True  # abrir la nueva categoría
        new_cat_input.value = ""
        new_cat_input.update()
        rebuild_tree()
        mostrar_status(f"+ {nombre}")

    def guardar(e):
        try:
            contenido = json.dumps(
                categorias_data, indent=2, ensure_ascii=False)
            with open(ruta_json, "w", encoding="utf-8") as f:
                f.write(contenido)
            local = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), PERFIL)
            if os.path.exists(local):
                with open(local, "w", encoding="utf-8") as f:
                    f.write(contenido)
            mostrar_status(f"💾 {PERFIL} guardado")
        except Exception as ex:
            mostrar_status(f"❌ Error: {ex}")

    def resetear(e):
        nonlocal categorias_data
        categorias_data = config.viewProfile(PERFIL)
        expanded.clear()
        rebuild_tree()
        mostrar_status("↩ restaurado")

    # ─── Construir tile de categoría ───

    def crear_tile(cat_name, exts, idx):
        # Row de extensiones (referencia persistente)
        ext_row = ft.Row(
            controls=(
                [crear_chip(e, cat_name) for e in sorted(exts)]
                if exts else
                [ft.Text("sin extensiones", size=11,
                         italic=True, color="#CCCCCC")]
            ),
            wrap=True, spacing=4, run_spacing=4,
            alignment=ft.MainAxisAlignment.END,
        )

        # Badge contador
        badge_text = ft.Text(str(len(exts)), size=10,
                             weight=ft.FontWeight.W_600, color=ACCENT)
        badge = ft.Container(
            content=badge_text, bgcolor=ACCENT_LIGHT,
            padding=ft.Padding(5, 1, 5, 1), border_radius=8,
        )

        # Input extensión
        ext_input = ft.TextField(
            hint_text="ext", dense=True,
            content_padding=ft.Padding(8, 4, 8, 4),
            text_size=11, hint_style=ft.TextStyle(size=11),
            border_color="#E0E0E0", focused_border_color=ACCENT,
            border_radius=4, width=80, height=30,
            on_submit=lambda e, c=cat_name: agregar_ext(
                c, e.control.value, e.control),
        )

        # Guardar refs
        cat_refs[cat_name] = {
            "ext_row": ext_row,
            "badge": badge_text,
            "input": ext_input,
        }

        body = ft.Container(
            content=ft.Column([
                ext_row,
                ft.Row([
                    ext_input,
                    ft.IconButton(icon=ft.Icons.ADD, icon_size=14, icon_color=ACCENT,
                                  tooltip="Añadir", width=28, height=28,
                                  on_click=lambda e, c=cat_name, i=ext_input: agregar_ext(c, i.value, i)),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=14,
                                  icon_color="#CCCCCC", tooltip="Eliminar categoría",
                                  width=28, height=28,
                                  on_click=lambda e, c=cat_name: eliminar_cat(c)),
                ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=6),
            padding=ft.Padding(36, 4, 12, 8),
        )

        def on_change(e, c=cat_name):
            expanded[c] = e.data == "true"

        tile = ft.ExpansionTile(
            leading=ft.Icon(icono_para(idx), size=16, color="#999999"),
            title=ft.Row([
                ft.Text(cat_name.replace("_", " "), size=13,
                        weight=ft.FontWeight.W_500, color="#333333"),
                badge,
            ], spacing=6),
            controls=[body],
            tile_padding=ft.Padding(12, 0, 12, 0),
            controls_padding=ft.Padding(0, 0, 0, 0),
            dense=True, min_tile_height=34,
            collapsed_bgcolor="#FFFFFF", bgcolor="#F7F7F7",
            icon_color="#BBBBBB", collapsed_icon_color="#DDDDDD",
            shape=ft.RoundedRectangleBorder(radius=0),
            collapsed_shape=ft.RoundedRectangleBorder(radius=0),
            maintain_state=True,
            expanded=expanded.get(cat_name, False),
            on_change=on_change,
        )

        return ft.DragTarget(
            group="ext", content=tile,
            on_accept=lambda e, c=cat_name: on_drop(e, c),
            on_will_accept=lambda e: True,
        )

    # ─── Rebuild completo (solo para crear/eliminar categorías) ───

    def rebuild_tree():
        tree_column.controls.clear()
        for idx, (cat, exts) in enumerate(categorias_data.items()):
            tree_column.controls.append(crear_tile(cat, exts, idx))
        tree_column.update()

    # ─── UI ───

    new_cat_input = ft.TextField(
        hint_text="Nueva categoría", dense=True,
        content_padding=ft.Padding(8, 4, 8, 4),
        text_size=12, hint_style=ft.TextStyle(size=12),
        border_color="#E0E0E0", focused_border_color=ACCENT,
        border_radius=4, expand=True, height=32,
        on_submit=crear_categoria,
    )

    # Render inicial
    for idx, (cat, exts) in enumerate(categorias_data.items()):
        tree_column.controls.append(crear_tile(cat, exts, idx))

    page.add(
        ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_TREE_OUTLINED,
                                size=16, color=ACCENT),
                        ft.Text(nombre_perfil, size=15,
                                weight=ft.FontWeight.W_600, color="#222222"),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.RESTART_ALT, icon_size=15,
                                      icon_color="#AAAAAA", tooltip="Restaurar",
                                      on_click=resetear, width=30, height=30),
                        ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, icon_size=15,
                                      icon_color=ACCENT, tooltip="Guardar",
                                      on_click=guardar, width=30, height=30),
                    ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(14, 10, 14, 6),
                ),
                # Nueva categoría
                ft.Container(
                    content=ft.Row([
                        new_cat_input,
                        ft.IconButton(icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                                      icon_size=16, icon_color=ACCENT,
                                      tooltip="Crear categoría",
                                      on_click=crear_categoria, width=30, height=30),
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(14, 0, 14, 4),
                ),
                # Status
                ft.Container(content=status_text, padding=ft.Padding(
                    14, 0, 14, 2), height=18),
                ft.Divider(height=1, color="#EEEEEE"),
                # Árbol
                ft.Container(content=tree_column,
                             expand=True, bgcolor="#FFFFFF"),
            ], spacing=0, expand=True),
            expand=True, bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E8E8E8"),
            border_radius=6, margin=ft.Margin(12, 12, 12, 12),
        )
    )


ft.run(main)
