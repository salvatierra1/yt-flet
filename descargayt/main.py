import flet as ft
import yt_dlp as youtube_dl

def main(page: ft.Page):
    
    # Título de la aplicación
    page.title = "DescargaYT"
    
    # Alineación centralizada
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
   
    # Habilitar el scroll
    page.scroll = True
    
    # Habilitar la adaptabilidad
    page.adaptive = True
    
    # Campo de texto para ingresar el enlace del video
    link = ft.TextField(label="Ingrese el enlace del video")
    
    # Barra de progreso
    progress = ft.ProgressBar(width=400, color="red", bgcolor="#eeeeee", visible=False)
    
    # Función para descargar el video
    def download(event):
        if not link.value:
            show_snackbar("Por favor ingrese un enlace de video.")
            return
        
        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
        }
        
        progress.visible = True
        page.update()
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(link.value, download=True)
                
                if 'entries' in result:
                    show_snackbar("Por favor ingrese solo enlaces de videos individuales, no listas de reproducción.")
                else:
                    progress.visible = False
                    show_dialog("Descarga completada", "El video se ha descargado exitosamente.")
                
            except youtube_dl.utils.DownloadError as e:
                progress.visible = False
                show_snackbar(f"Error: No se pudo descargar el video. Detalles: {str(e)}")
        
        link.value = ""
        page.update()
    
    # Función para mostrar un Snackbar con un mensaje
    def show_snackbar(message):
        snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.WHITE), bgcolor=ft.colors.BLACK38)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    # Función para mostrar un diálogo con un mensaje
    def show_dialog(title, message):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    # Función para mostrar la sección de descarga
    def show_download_section(event):
        body = ft.SafeArea(
            content= ft.Column(
                [
                    ft.Text("Inicie su descarga 📥"),
                    link,
                    progress,
                    ft.ElevatedButton("Descargar", on_click=download, icon=ft.icons.PLAY_CIRCLE, bgcolor=ft.colors.RED_900, color=ft.colors.WHITE70)
                ]
            )
        )
        
        # Limpia la página y agrega la sección de descarga
        page.clean()
        page.add(body)
        page.update()
    
    # Configuración de la barra de aplicación (app bar)
    page.appbar = ft.AppBar(
        leading=ft.TextButton("YT", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("DescargaYT"),
        actions=[
            ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0), on_click=show_download_section)
        ],
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
    )
    
    # Configuración de la barra de navegación (navigation bar)
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="YouTube"),
            ft.NavigationBarDestination(icon=ft.icons.LIST, label="Descargas"),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
        ),
    )
    
    # Actualizar la página inicialmente
    page.update()

# Iniciar la aplicación
ft.app(main)
