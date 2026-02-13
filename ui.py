from main import Configuracion
import flet as ft
from tkinter import filedialog
import pyperclip


def main(page: ft.Page):
    nombreAPP = "My Optimizer"
    page.title = nombreAPP
    page.theme = ft.Theme(color_scheme_seed="#2979FF", use_material3=True)
    config = Configuracion()
    destinyRef = ft.Ref[ft.Text]()

    async def pickFiles(e):
        selectedDirectory = filedialog.askdirectory(title="Seleccionar carpeta")
        config.setDestinyPath(selectedDirectory)
        destinyRef.current.value = "Ruta de destino: " + config.destinyPath
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
                                            ft.Text("■", color=ft.Colors.BLUE, size=30),
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
                                    content=ft.Container(
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=6
                                        ),
                                        bgcolor="#1E1E1E",  # fondo oscuro similar al ejemplo
                                        border_radius=20,
                                        content=ft.Row(
                                            spacing=8,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    width=10,
                                                    height=10,
                                                    bgcolor=ft.Colors.GREEN,
                                                    border_radius=50,  # círculo perfecto
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
                                controls=[
                                    ft.Text(
                                        "Ruta de destino para los archivos optimizados:",
                                        color="#8B9EAF",
                                        size=14,
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
                            width=400000,
                            content=ft.Container(
                                padding=ft.padding.symmetric(
                                    horizontal=16, vertical=12
                                ),
                                border_radius=15,
                                border=ft.border.all(
                                    2, "#333333"
                                ),  # borde gris muy oscuro
                                bgcolor="#00072E",  # fondo oscuro tipo terminal
                                content=ft.GestureDetector(
                                    on_tap=pickFiles,
                                    mouse_cursor=ft.MouseCursor.CLICK,
                                    content=ft.Text(
                                        (
                                            config.destinyPath
                                            if config.destinyPath
                                            else "Ninguna carpeta seleccionada"
                                        ),
                                        ref=destinyRef,
                                        size=14,
                                    ),
                                ),
                            ),
                        ),
                    ]
                ),
            ),
        )

    def profilesUI():
        return ft.Card()

    def previewUI():
        return ft.Card()

    """
        page.add(ft.Column(
            controls=[
                ft.Text("Donde quieres que se guarden los ficheros:"),
                ft.Column(
                    ref=destinyRef,
                    controls=[
                        ft.ElevatedButton(ft.Icon(ft.Icons.FOLDER, color=ft.Colors.BLUE), on_click=pickFiles),
                        ft.Text("Ninguna carpeta seleccionada")
                    ]
                )
            ]
        ))
        """

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
        ft.Column(
            controls=[
                systemUI(),
                profilesUI(),
                previewUI(),
            ]
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)
