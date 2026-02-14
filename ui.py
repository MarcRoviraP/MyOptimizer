from main import Configuracion
import flet as ft
from tkinter import filedialog
import pyperclip


def main(page: ft.Page):
    nombreAPP = "My Optimizer"
    page.title = nombreAPP
    page.theme = ft.Theme(
        use_material3=False,
        card_bgcolor="#1A202E",
    )
    config = Configuracion()
    destinyRef = ft.Ref[ft.Text]()
    foldersRef = ft.Ref[ft.GridView]()

    async def pickFiles(e):
        selectedDirectory = filedialog.askdirectory(title="Seleccionar carpeta")
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

    def añadirCarpeta():
        selectedDirectory = filedialog.askdirectory(title="Seleccionar carpeta")
        if selectedDirectory:
            if config.addFolderToStructure(selectedDirectory):
                foldersRef.current.controls.append(
                    ft.Card(
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
                                        selectedDirectory.split("/")[-1],
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
                )
                foldersRef.current.update()

    def folderOrganizerUI():
        listaCarpetas = config.folderStructure

        # Crear las tarjetas dinámicas de las carpetas
        carpeta_cards = [
            ft.Card(
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
                                carpeta,
                                color=ft.Colors.WHITE,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
            )
            for carpeta in listaCarpetas
        ]

        # Tarjeta fija para "Agregar carpeta"
        agregar_card = ft.Card(
            elevation=2,
            bgcolor="#0000FF40",
            shape=ft.RoundedRectangleBorder(radius=10),
            content=ft.GestureDetector(
                on_tap=añadirCarpeta,
                mouse_cursor=ft.MouseCursor.CLICK,
                content=ft.Container(
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    content=ft.Column(
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                align=ft.alignment.Alignment.CENTER,
                                icon=ft.Icons.ADD,
                                color=ft.Colors.BLUE,
                                size=20,
                            ),
                            ft.Text(
                                "Agregar carpeta",
                                align=ft.alignment.Alignment.CENTER,
                                color=ft.Colors.BLUE,
                                size=14,
                                weight=ft.FontWeight.BOLD,
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

    def profilesUI():
        return ft.Card()

    def previewUI():
        return ft.Card()

    page.bgcolor = "#101622"
    page.add(
        ft.Card(
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
