import flet as ft

def main(page: ft.Page):
    page.title = "Test Dialog"
    
    def mostrar_dialogo(e):
        def cerrar_dlg(e):
            dlg.open = False
            dlg.update()  # ✅ Actualizar el diálogo mismo
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Prueba"),
            content=ft.Text("¿Funciona el diálogo?"),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_dlg)
            ]
        )
        
        page.overlay.append(dlg)  # ✅ Agregar a overlay
        dlg.open = True
        page.update()
    
    page.add(
        ft.Button("Probar diálogo", on_click=mostrar_dialogo)
    )

ft.run(main)