from logging import root
from main import Configuracion
import flet as ft
from tkinter import filedialog
import tkinter as tk
import pyperclip
import shutil
import os
import json


def main(page: ft.Page):
    nombreAPP = "My Optimizer"
    page.title = nombreAPP

    config = Configuracion()
    destinyRef = ft.Ref[ft.Text]()
    foldersRef = ft.Ref[ft.GridView]()
    profilesRef = ft.Ref[ft.Column]()
    nombrePerfil = ft.Ref[ft.TextField]()
    contadorPerfilesRef = ft.Ref[ft.Text]()
    editContainerPreviewRef = ft.Ref[ft.Container]()

    profileSelected = config.getProfiles()[0] if config.getProfiles() else None

    def seleccionar_carpeta():
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        root.attributes("-topmost", True)  # 👈 Siempre arriba

        selectedDirectory = filedialog.askdirectory(
            parent=root, title="Seleccionar carpeta"
        )

        root.destroy()
        return selectedDirectory

    async def pickFiles(e):
        selectedDirectory = seleccionar_carpeta()
        config.setDestinyPath(selectedDirectory)
        destinyRef.current.value = (
            config.destinyPath if config.destinyPath else "Ninguna carpeta seleccionada"
        )
        destinyRef.current.update()

    def copiarRutaPortapapeles(e):
        print(config.destinyPath)
        pyperclip.copy(config.destinyPath)

    def systemUI():
        return ft.Card(
            bgcolor="#1A202E",
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.SETTINGS,
                                                color=ft.Colors.BLUE,
                                                size=30,
                                            ),
                                            ft.Text(
                                                "Configuración del sistema",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ]
                                    )
                                ),
                                ft.Card(
                                    elevation=2,
                                    bgcolor="#3000FF40",
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    content=ft.Container(
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=6
                                        ),
                                        content=ft.Row(
                                            spacing=8,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    width=10,
                                                    height=10,
                                                    bgcolor=ft.Colors.GREEN,
                                                    border_radius=50,
                                                ),
                                                ft.Text(
                                                    "Active",
                                                    color=ft.Colors.GREEN,
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                        ),
                                    ),
                                ),
                            ],
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Ruta de destino para los archivos optimizados:",
                                        color="#8B9EAF",
                                        size=14,
                                        expand=True,
                                    ),
                                    ft.GestureDetector(
                                        on_tap=copiarRutaPortapapeles,
                                        mouse_cursor=ft.MouseCursor.CLICK,
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.COPY,
                                                    color=ft.Colors.BLUE,
                                                    size=20,
                                                ),
                                                ft.Text(
                                                    "Copiar ruta",
                                                    color=ft.Colors.BLUE,
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ]
                                        ),
                                    ),
                                ],
                            )
                        ),
                        ft.Card(
                            elevation=0,
                            width=500,
                            content=ft.Container(
                                padding=ft.padding.symmetric(
                                    horizontal=16, vertical=12
                                ),
                                border_radius=15,
                                border=ft.border.all(
                                    2, "#333333"
                                ),  # borde gris muy oscuro
                                bgcolor="#0D121C",  # fondo oscuro tipo terminal
                                content=ft.GestureDetector(
                                    on_tap=pickFiles,
                                    mouse_cursor=ft.MouseCursor.CLICK,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                (
                                                    config.destinyPath
                                                    if config.destinyPath
                                                    else "Ninguna carpeta seleccionada"
                                                ),
                                                ref=destinyRef,
                                                size=14,
                                            ),
                                            ft.Icon(
                                                ft.Icons.ARROW_DROP_DOWN,
                                                color=ft.Colors.BLUE,
                                                size=20,
                                            ),
                                        ],
                                    ),
                                ),
                            ),
                        ),
                    ]
                ),
            ),
        )

    def uiCustomFolderCard(carpeta):
        return ft.Card(
            elevation=2,
            bgcolor="#3000FF40",
            shape=ft.RoundedRectangleBorder(radius=10),
            content=ft.Container(
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                content=ft.Column(
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.FOLDER,
                            color=ft.Colors.YELLOW,
                            size=20,
                        ),
                        ft.Text(
                            carpeta.split("/")[-1],
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=ft.Colors.WHITE,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
            ),
        )

    def añadirCarpeta():
        selectedDirectory = seleccionar_carpeta()
        if selectedDirectory:
            if config.addFolderToStructure(selectedDirectory):
                foldersRef.current.controls.append(
                    uiCustomFolderCard(selectedDirectory)
                )
                foldersRef.current.update()

    def folderOrganizerUI():
        listaCarpetas = config.folderStructure

        # Crear las tarjetas dinámicas de las carpetas
        carpeta_cards = [uiCustomFolderCard(
            carpeta) for carpeta in listaCarpetas]

        # Tarjeta fija para "Agregar carpeta"
        agregar_card = ft.Card(
            elevation=2,
            bgcolor="#0000FF40",
            shape=ft.RoundedRectangleBorder(
                radius=10,
                side=ft.BorderSide(2, ft.Colors.BLUE),
            ),
            content=ft.GestureDetector(
                on_tap=añadirCarpeta,
                mouse_cursor=ft.MouseCursor.CLICK,
                content=ft.Container(
                    padding=ft.padding.symmetric(horizontal=12, vertical=12),
                    content=ft.Column(
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                icon=ft.Icons.ADD,
                                color=ft.Colors.BLUE,
                                size=30,
                            ),
                            ft.Text(
                                "Agregar carpeta",
                                color=ft.Colors.BLUE,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                width=float("inf"),
                            ),
                        ],
                    ),
                ),
            ),
        )

        todas_las_cards = carpeta_cards + [agregar_card]

        # GridView responsive
        return ft.Container(
            expand=True,  # que ocupe todo el espacio disponible
            height=400,  # altura fija para el GridView
            padding=ft.padding.all(10),
            content=ft.GridView(
                ref=foldersRef,
                runs_count=None,  # permite que las columnas se ajusten al ancho disponible
                max_extent=180,  # ancho máximo por tarjeta
                spacing=8,
                run_spacing=8,
                controls=todas_las_cards,
                expand=True,  # que el GridView crezca con el contenedor
            ),
        )

    def onPerfilClick(e, perfil):
        nonlocal profileSelected
        profileSelected = perfil
        print(f"✨ Perfil seleccionado: {perfil}")

        # Animación suave al seleccionar
        for control in profilesRef.current.controls[1].controls:
            if isinstance(control, ft.Container):
                tile = control.content
                is_selected = tile.title.value == perfil.replace("config_", "").replace(
                    ".json", ""
                )

                # Efecto visual mejorado
                control.bgcolor = (
                    ft.Colors.with_opacity(0.15, ft.Colors.BLUE)
                    if is_selected
                    else None
                )
                control.border = (
                    ft.border.all(
                        2, ft.Colors.BLUE_400) if is_selected else None
                )
                control.shadow = (
                    ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                        offset=ft.Offset(0, 2),
                    )
                    if is_selected
                    else None
                )

                control.update()

        # Actualizar vista previa al seleccionar
        tooglePreviewView(None, perfil, False)

    def dialogSeguroEliminarPerfil(perfil):
        nombre_perfil = perfil.replace("config_", "").replace(".json", "")
        print(f"⚠️ Confirmar eliminación del perfil: {nombre_perfil}")

        def eliminarPerfilConfirmado(e):
            dlg.open = False
            page.update()
            onDeletePerfil(e, perfil)

        def cerrar_dialog(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.WARNING_ROUNDED,
                            color=ft.Colors.ORANGE, size=28),
                    ft.Text("Confirmar eliminación",
                            weight=ft.FontWeight.BOLD),
                ]
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "¿Estás seguro de que quieres eliminar el perfil:", size=14
                        ),
                        ft.Container(
                            content=ft.Text(
                                nombre_perfil,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                            bgcolor=ft.Colors.with_opacity(
                                0.1, ft.Colors.BLUE),
                            padding=ft.Padding(10, 10, 10, 10),
                            border_radius=8,
                            margin=ft.Margin(0, 10, 0, 10),
                        ),
                        ft.Text(
                            "⚠️ Esta acción no se puede deshacer.",
                            size=13,
                            color=ft.Colors.RED_700,
                            italic=True,
                        ),
                    ],
                    tight=True,
                    spacing=5,
                ),
                width=350,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.FilledButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE_FOREVER,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE
                    ),
                    on_click=eliminarPerfilConfirmado,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg)  # ✅ Agregar al overlay
        dlg.open = True  # ✅ Abrir
        page.update()  # ✅ Actualizar

    def onDeletePerfil(e, perfil):
        print(f"🗑️ Eliminando perfil: {perfil}")
        os.remove(os.path.join(config.RUTA_CONFIG, perfil))
        # Eliminar de la UI
        profilesRef.current.controls[1].controls = [
            c
            for c in profilesRef.current.controls[1].controls
            if not (
                isinstance(c, ft.Container)
                and c.content.title.value
                == perfil.replace("config_", "").replace(".json", "")
            )
        ]
        contadorPerfilesRef.current.value = str(
            int(contadorPerfilesRef.current.value) - 1
        )
        contadorPerfilesRef.current.update()
        profilesRef.current.update()

    def viewEditarPerfil(perfil):
        ACCENT = "#4C8BF5"
        ACCENT_LIGHT = "#1A2A4A"
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

        nombre = perfil.replace("config_", "").replace(".json", "")
        perfilData = config.viewProfile(perfil)
        ruta_json = os.path.join(config.RUTA_CONFIG, perfil)

        cat_refs = {}
        exp_state = {}
        tree_col = ft.Column(spacing=0, scroll="auto")
        status = ft.Text("", size=11, color="#8B9EAF", italic=True)

        def set_status(msg):
            status.value = msg
            status.update()

        def icon_for(i):
            return ICON_POOL[i % len(ICON_POOL)]

        # ── Chip de extensión (arrastrable) ──

        def make_chip(ext, cat):
            return ft.Draggable(
                group="ext",
                data={"ext": ext, "from": cat},
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f".{ext}", size=11, weight=ft.FontWeight.W_500,
                                    color="#C0C8D4", font_family="Consolas"),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE, icon_size=10,
                                icon_color="#667788", tooltip="Quitar",
                                on_click=lambda e, c=cat, x=ext: remove_ext(
                                    c, x),
                                width=20, height=20,
                            ),
                        ],
                        spacing=2, tight=True,
                    ),
                    bgcolor="#1A202E",
                    padding=ft.Padding(6, 2, 2, 2),
                    border_radius=4,
                    border=ft.Border.all(1, "#222222"),
                ),
            )

        # ── Actualización in-place (NO reconstruye el tile) ──

        def update_cat_ui(cat):
            ref = cat_refs.get(cat)
            if not ref:
                return
            exts = perfilData.get(cat, [])
            row = ref["ext_row"]
            row.controls.clear()
            if exts:
                for e in sorted(exts):
                    row.controls.append(make_chip(e, cat))
            else:
                row.controls.append(
                    ft.Text("sin extensiones", size=11,
                            italic=True, color="#556677")
                )
            row.update()
            ref["badge"].value = str(len(exts))
            ref["badge"].update()

        # ── Acciones ──

        def add_ext(cat, val, inp):
            ext = val.strip().lower().lstrip(".")
            if not ext:
                return
            if ext in perfilData[cat]:
                set_status(f"⚠ .{ext} ya existe en {cat.replace('_', ' ')}")
                return
            perfilData[cat].append(ext)
            inp.value = ""
            inp.update()
            update_cat_ui(cat)
            set_status(f"+ .{ext} → {cat.replace('_', ' ')}")

        def remove_ext(cat, ext):
            if ext in perfilData[cat]:
                perfilData[cat].remove(ext)
            update_cat_ui(cat)
            set_status(f"− .{ext} de {cat.replace('_', ' ')}")

        def on_drop(e, cat_dest):
            src = page.get_control(e.src_id)
            data = src.data
            if isinstance(data, str):
                data = json.loads(data)
            ext = data["ext"]
            cat_src = data["from"]
            if cat_src == cat_dest:
                return
            if ext in perfilData[cat_src]:
                perfilData[cat_src].remove(ext)
            if ext not in perfilData[cat_dest]:
                perfilData[cat_dest].append(ext)
            update_cat_ui(cat_src)
            update_cat_ui(cat_dest)
            set_status(
                f".{ext}  {cat_src.replace('_', ' ')} → {cat_dest.replace('_', ' ')}")

        def delete_cat(cat):
            if cat in perfilData:
                del perfilData[cat]
            cat_refs.pop(cat, None)
            exp_state.pop(cat, None)
            rebuild()
            set_status(f"✕ {cat.replace('_', ' ')} eliminada")

        def create_cat(e):
            n = new_input.value.strip()
            if not n:
                return
            key = n.replace(" ", "_")
            if key in perfilData:
                set_status(f"⚠ '{n}' ya existe")
                return
            perfilData[key] = []
            exp_state[key] = True
            new_input.value = ""
            new_input.update()
            rebuild()
            set_status(f"+ {n}")

        def save(e):
            try:
                contenido = json.dumps(
                    perfilData, indent=2, ensure_ascii=False)
                with open(ruta_json, "w", encoding="utf-8") as f:
                    f.write(contenido)
                local = os.path.join(os.path.dirname(
                    os.path.abspath(__file__)), perfil)
                if os.path.exists(local):
                    with open(local, "w", encoding="utf-8") as f:
                        f.write(contenido)
                set_status(f"💾 {perfil} guardado")
            except Exception as ex:
                set_status(f"❌ Error: {ex}")

        def reset(e):
            nonlocal perfilData
            perfilData.clear()
            perfilData.update(config.viewProfile(perfil))
            exp_state.clear()
            rebuild()
            set_status("↩ restaurado")

        # ── Crear tile de categoría ──

        def make_tile(cat, exts, idx):
            ext_row = ft.Row(
                controls=(
                    [make_chip(e, cat) for e in sorted(exts)]
                    if exts else
                    [ft.Text("sin extensiones", size=11,
                             italic=True, color="#556677")]
                ),
                wrap=True, spacing=4, run_spacing=4,
                alignment=ft.MainAxisAlignment.END,
            )
            badge_txt = ft.Text(str(len(exts)), size=10,
                                weight=ft.FontWeight.W_600, color=ACCENT)
            badge = ft.Container(content=badge_txt, bgcolor=ACCENT_LIGHT,
                                 padding=ft.Padding(5, 1, 5, 1), border_radius=8)

            ext_inp = ft.TextField(
                hint_text="ext", dense=True,
                content_padding=ft.Padding(8, 4, 8, 4),
                text_size=11, hint_style=ft.TextStyle(size=11, color="#556677"),
                color="#E0E6ED", bgcolor="#1A202E",
                border_color="#222222", focused_border_color=ACCENT,
                border_radius=4, width=80, height=30,
                on_submit=lambda e, c=cat: add_ext(
                    c, e.control.value, e.control),
            )

            cat_refs[cat] = {"ext_row": ext_row,
                             "badge": badge_txt, "input": ext_inp}

            body = ft.Container(
                content=ft.Column([
                    ext_row,
                    ft.Row([
                        ext_inp,
                        ft.IconButton(icon=ft.Icons.ADD, icon_size=14, icon_color=ACCENT,
                                      tooltip="Añadir", width=28, height=28,
                                      on_click=lambda e, c=cat, i=ext_inp: add_ext(c, i.value, i)),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=14,
                                      icon_color="#667788", tooltip="Eliminar categoría",
                                      width=28, height=28,
                                      on_click=lambda e, c=cat: delete_cat(c)),
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ], spacing=6),
                padding=ft.Padding(36, 4, 12, 8),
            )

            def on_change(e, c=cat):
                exp_state[c] = e.data == "true"

            tile = ft.ExpansionTile(
                leading=ft.Icon(icon_for(idx), size=16, color="#8B9EAF"),
                title=ft.Row([
                    ft.Text(cat.replace("_", " "), size=13,
                            weight=ft.FontWeight.W_500, color="#C0C8D4"),
                    badge,
                ], spacing=6),
                controls=[body],
                tile_padding=ft.Padding(12, 0, 12, 0),
                controls_padding=ft.Padding(0, 0, 0, 0),
                dense=True, min_tile_height=34,
                collapsed_bgcolor="#151B27", bgcolor="#0D121C",
                icon_color="#8B9EAF", collapsed_icon_color="#556677",
                shape=ft.RoundedRectangleBorder(radius=0),
                collapsed_shape=ft.RoundedRectangleBorder(radius=0),
                maintain_state=True,
                expanded=exp_state.get(cat, False),
                on_change=on_change,
            )

            return ft.DragTarget(
                group="ext", content=tile,
                on_accept=lambda e, c=cat: on_drop(e, c),
                on_will_accept=lambda e: True,
            )

        # ── Rebuild (solo para crear/eliminar categorías) ──

        def rebuild():
            tree_col.controls.clear()
            for i, (c, exts) in enumerate(perfilData.items()):
                tree_col.controls.append(make_tile(c, exts, i))
            tree_col.update()

        # ── Input nueva categoría ──

        new_input = ft.TextField(
            hint_text="Nueva categoría", dense=True,
            content_padding=ft.Padding(8, 4, 8, 4),
            text_size=12, hint_style=ft.TextStyle(size=12, color="#556677"),
            color="#E0E6ED", bgcolor="#1A202E",
            border_color="#222222", focused_border_color=ACCENT,
            border_radius=4, expand=True, height=32,
            on_submit=create_cat,
        )

        # Render inicial
        for i, (c, exts) in enumerate(perfilData.items()):
            tree_col.controls.append(make_tile(c, exts, i))

        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_TREE_OUTLINED,
                                size=16, color=ACCENT),
                        ft.Text(nombre, size=15,
                                weight=ft.FontWeight.W_600, color="#E0E6ED"),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.RESTART_ALT, icon_size=15,
                                      icon_color="#667788", tooltip="Restaurar",
                                      on_click=reset, width=30, height=30),
                        ft.IconButton(icon=ft.Icons.SAVE_OUTLINED, icon_size=15,
                                      icon_color=ACCENT, tooltip="Guardar",
                                      on_click=save, width=30, height=30),
                    ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(14, 10, 14, 6),
                ),
                # Nueva categoría
                ft.Container(
                    content=ft.Row([
                        new_input,
                        ft.IconButton(icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                                      icon_size=16, icon_color=ACCENT,
                                      tooltip="Crear categoría",
                                      on_click=create_cat, width=30, height=30),
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(14, 0, 14, 4),
                ),
                # Status
                ft.Container(content=status, padding=ft.Padding(
                    14, 0, 14, 2), height=18),
                ft.Divider(height=1, color="#333333"),
                # Árbol
                ft.Container(content=tree_col, expand=True, bgcolor="#1A202E"),
            ], spacing=0, expand=True),
            height=620,
            bgcolor="#1A202E",
            border=ft.Border.all(1, "#333333"),
            border_radius=6,
        )

    def viewPreviewPerfil(perfil):
        return ft.Card()

    def tooglePreviewView(e, perfil, vistaEditar):

        if vistaEditar:
            print(f"🔍 Vista previa del perfil: {perfil} (modo edición)")
            editContainerPreviewRef.current.content = viewEditarPerfil(perfil)
        else:
            print(f"🔍 Vista previa del perfil: {perfil}")
            editContainerPreviewRef.current.content = viewPreviewPerfil(perfil)

    def createProfileUI(perfil):
        return ft.Container(
            content=ft.ListTile(
                title=ft.Text(
                    perfil.replace("config_", "").replace(".json", ""),
                    size=15,
                    weight=ft.FontWeight.W_500,
                ),
                leading=ft.Container(
                    content=ft.Icon(
                        ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.BLUE_400, size=28
                    ),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                    border_radius=25,
                    width=45,
                    height=45,
                    alignment=ft.alignment.Alignment.CENTER,
                ),
                trailing=ft.Container(  # ✅ Envolver en Container
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_size=18,
                                icon_color=ft.Colors.GREEN_400,
                                tooltip="Editar perfil",
                                on_click=lambda e, p=perfil: tooglePreviewView(
                                    e, p, True),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_size=18,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Eliminar perfil",
                                on_click=lambda e, p=perfil: dialogSeguroEliminarPerfil(
                                    p),
                            ),
                        ],
                        spacing=0,  # ✅ Sin espacio entre botones
                        tight=True,  # ✅ Compacto
                    ),
                ),
                on_click=lambda e, p=perfil: onPerfilClick(e, p),
            ),
            bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.GREY),
            border_radius=12,
            padding=5,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            ink=True,
            on_hover=lambda e: setattr(
                e.control,
                "bgcolor",
                (
                    ft.Colors.with_opacity(0.08, ft.Colors.GREY)
                    if e.data == "true"
                    else ft.Colors.with_opacity(0.03, ft.Colors.GREY)
                ),
            )
            or e.control.update(),
        )

    def setupProfiles():
        perfiles = config.getProfiles()

        return ft.Column(
            ref=profilesRef,
            spacing=8,
            height=470,
            controls=[
                # Header con estilo
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.FOLDER_SPECIAL,
                                color=ft.Colors.BLUE_400,
                                size=24,
                            ),
                            ft.Text(
                                "Mis Perfiles",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    str(len(perfiles)),
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    ref=contadorPerfilesRef,
                                ),
                                bgcolor=ft.Colors.BLUE_400,
                                border_radius=10,
                                padding=ft.padding.symmetric(
                                    horizontal=8, vertical=2),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=10,
                ),
                # Lista de perfiles con cards
                ft.ListView(
                    expand=True,
                    spacing=8,
                    padding=10,
                    controls=[createProfileUI(perfil) for perfil in perfiles],
                ),
            ],
        )

    def addProfile():
        nombre = nombrePerfil.current.value.strip()
        if not nombre:
            return

        perfiles = config.getProfiles()
        if f"config_{nombre}.json" in perfiles:
            print("⚠️ Ya existe un perfil con ese nombre.")
            return

        shutil.copy(
            "config_Optimizador.json",
            os.path.join(config.RUTA_CONFIG, f"config_{nombre}.json"),
        )
        profilesRef.current.controls[1].controls.append(
            createProfileUI(f"config_{nombre}.json")
        )
        contadorPerfilesRef.current.value = str(len(perfiles) + 1)
        contadorPerfilesRef.current.update()

    def profilesUI():
        return ft.Card(
            bgcolor="#1A202E",
            width=400,
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Perfiles de optimización",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Divider(),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.TextField(
                                    hint_text="Nombre del perfil",
                                    expand=True,
                                    bgcolor="#0D121C",
                                    border=ft.border.all(2, "#333333"),
                                    ref=nombrePerfil,
                                ),
                                ft.IconButton(
                                    ft.Icons.ADD, bgcolor="#2B6CEE", on_click=addProfile
                                ),
                            ],
                        ),
                        ft.Divider(),
                        setupProfiles(),
                    ]
                ),
            ),
        )

    def previewUI():
        return ft.Card(
            bgcolor="#1A202E",
            content=ft.Container(padding=20, ref=editContainerPreviewRef),
        )

    page.bgcolor = "#101622"
    page.window.height = 820
    page.add(
        ft.Card(
            bgcolor="#1A202E",
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Icon(ft.Icons.SPEED, color=ft.Colors.BLUE, size=40),
                        ft.Text(nombreAPP, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Workspace",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE,
                        ),
                    ],
                ),
            ),
        ),
        ft.Row(
            alignment="start",
            vertical_alignment="start",
            controls=[
                ft.Column(
                    controls=[systemUI(), folderOrganizerUI()],
                    expand=True,
                ),
                ft.Column(
                    controls=[profilesUI()],
                    expand=True,
                ),
                ft.Column(
                    controls=[previewUI()],
                    expand=True,
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)
