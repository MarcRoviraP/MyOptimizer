from logging import root
from main import Configuracion
import flet as ft
from tkinter import filedialog
import tkinter as tk
import pyperclip
import shutil
import os

def main(page: ft.Page):
    nombreAPP = "My Optimizer"
    page.title = nombreAPP

    config = Configuracion()
    destinyRef = ft.Ref[ft.Text]()
    foldersRef = ft.Ref[ft.GridView]()
    profilesRef = ft.Ref[ft.Column]()
    nombrePerfil = ft.Ref[ft.TextField]()
    contadorPerfilesRef = ft.Ref[ft.Text]()
    editPreviewRef = ft.Ref[ft.Text]()
    
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
        carpeta_cards = [uiCustomFolderCard(carpeta) for carpeta in listaCarpetas]

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
                is_selected = tile.title.value == perfil.replace("config_", "").replace(".json", "")

                # Efecto visual mejorado
                control.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.BLUE) if is_selected else None
                control.border = ft.border.all(2, ft.Colors.BLUE_400) if is_selected else None
                control.shadow = ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                    offset=ft.Offset(0, 2)
                ) if is_selected else None

                control.update()

    def dialogSeguroEliminarPerfil(perfil):
        nombre_perfil = perfil.replace('config_', '').replace('.json', '')
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
                    ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.ORANGE, size=28),
                    ft.Text("Confirmar eliminación", weight=ft.FontWeight.BOLD)
                ]
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "¿Estás seguro de que quieres eliminar el perfil:",
                            size=14
                        ),
                        ft.Container(
                            content=ft.Text(
                                nombre_perfil,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700
                            ),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                            padding=ft.Padding(10, 10, 10, 10),
                            border_radius=8,
                            margin=ft.Margin(0, 10, 0, 10)
                        ),
                        ft.Text(
                            "⚠️ Esta acción no se puede deshacer.",
                            size=13,
                            color=ft.Colors.RED_700,
                            italic=True
                        )
                    ],
                    tight=True,
                    spacing=5
                ),
                width=350
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.FilledButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE_FOREVER,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE
                    ),
                    on_click=eliminarPerfilConfirmado
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg)  # ✅ Agregar al overlay
        dlg.open = True     # ✅ Abrir
        page.update()       # ✅ Actualizar            
    
    def onDeletePerfil(e, perfil):
        print(f"🗑️ Eliminando perfil: {perfil}")
        os.remove(os.path.join(config.RUTA_CONFIG, perfil))
        # Eliminar de la UI
        profilesRef.current.controls[1].controls = [
            c for c in profilesRef.current.controls[1].controls
            if not (isinstance(c, ft.Container) and c.content.title.value == perfil.replace("config_", "").replace(".json", ""))
        ]
        contadorPerfilesRef.current.value = str(int(contadorPerfilesRef.current.value) - 1)
        contadorPerfilesRef.current.update()
        profilesRef.current.update()
    
    def createProfileUI(perfil):
        return ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(
                                    perfil.replace("config_", "").replace(".json", ""),
                                    size=15,
                                    weight=ft.FontWeight.W_500
                                ),
                                leading=ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ACCOUNT_CIRCLE,
                                        color=ft.Colors.BLUE_400,
                                        size=28
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                                    border_radius=25,
                                    width=45,
                                    height=45,
                                    alignment=ft.alignment.Alignment.CENTER
                                ),
                                trailing=ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED_400,
                                    on_click=lambda e, p=perfil: dialogSeguroEliminarPerfil(p)
                                ),
                                on_click=lambda e, p=perfil: onPerfilClick(e, p),
                            ),
                            bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.GREY),
                            border_radius=12,
                            padding=5,
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                            ink=True,
                            on_hover=lambda e: setattr(e.control, 'bgcolor', 
                                ft.Colors.with_opacity(0.08, ft.Colors.GREY) if e.data == "true" 
                                else ft.Colors.with_opacity(0.03, ft.Colors.GREY)) or e.control.update()
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
                            ft.Icon(ft.Icons.FOLDER_SPECIAL, color=ft.Colors.BLUE_400, size=24),
                            ft.Text(
                                "Mis Perfiles",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700
                            ),
                            ft.Container(
                                content=ft.Text(
                                    
                                    str(len(perfiles)),
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    ref=contadorPerfilesRef
                                ),
                                bgcolor=ft.Colors.BLUE_400,
                                border_radius=10,
                                padding=ft.padding.symmetric(horizontal=8, vertical=2)
                            )
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
                    controls=[
                        createProfileUI(perfil)
                        for perfil in perfiles
                    ],
                ),
            ]
        )

    def addProfile():
        nombre = nombrePerfil.current.value.strip()
        if not nombre: return
        
        perfiles = config.getProfiles()
        if f"config_{nombre}.json" in perfiles:
            print("⚠️ Ya existe un perfil con ese nombre.")
            return
        
        shutil.copy("config_Optimizador.json", os.path.join(config.RUTA_CONFIG, f"config_{nombre}.json"))
        profilesRef.current.controls[1].controls.append(createProfileUI(f"config_{nombre}.json"))
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
                                    ft.Icons.ADD,
                                    bgcolor="#2B6CEE",
                                    on_click=addProfile
                                ),
                            ],
                        ),
                        
                        ft.Divider(),
                        setupProfiles()
                    ]
                ),
            ),
        )

    def previewUI():
        return ft.Card(
            bgcolor="#1A202E",
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
    
