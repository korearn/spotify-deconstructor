import os
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Inicializamos la consola de rich para los estilos
console = Console()

def generar_nota_obsidian():
    console.print(Panel.fit("[bold green]🎧 Spotify Deconstructor[/bold green]", border_style="green"))
    
    load_dotenv()
    
    # Validación amigable de credenciales
    if not os.getenv("SPOTIPY_CLIENT_ID") or not os.getenv("SPOTIPY_CLIENT_SECRET"):
        console.print("[bold red]¡Alto ahí![/bold red] Faltan tus credenciales de Spotify.")
        console.print("Revisa el archivo [cyan]README.md[/cyan] para ver cómo configurar tu archivo [yellow].env[/yellow].")
        return

    # Animación de carga mientras hace el request a la API
    with console.status("[bold green]Analizando tus frecuencias recientes...[/bold green]", spinner="dots"):
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                scope="user-top-read",
                open_browser=False
            ))
            resultados = sp.current_user_top_tracks(limit=10, time_range='short_term')
        except Exception as e:
            console.print(f"[bold red]Error al conectar con la API de Spotify:[/bold red] {e}")
            return

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"Influencias_{fecha_hoy}.md"
    
    # Preparamos la tabla visual para la terminal
    tabla = Table(title="Top 10 Tracks a Deconstruir", title_style="bold magenta")
    tabla.add_column("#", justify="right", style="cyan", no_wrap=True)
    tabla.add_column("Track", style="white")
    tabla.add_column("Artista", style="green")

    contenido_md = f"""---
fecha: {fecha_hoy}
tipo: extraccion_musical
tags: [musica/influencias, deconstruccion]
---

# Radar de Influencias - {fecha_hoy}

Aquí están las pistas que más han estado sonando recientemente. Listo para analizar texturas, tempos y arreglos para aplicar al proyecto musical.

## Top 10 Tracks
"""
    
    for i, cancion in enumerate(resultados.get('items', [])):
        nombre = cancion.get('name', 'Desconocido')
        artista = cancion['artists'][0].get('name', 'Desconocido')
        
        # Agregamos la fila a la tabla de la terminal
        tabla.add_row(str(i + 1), nombre, artista)
        
        # Agregamos el checkbox al Markdown
        contenido_md += f"- [ ] **{nombre}** - *{artista}*\n"
        
    contenido_md += """
---
### Notas de Deconstrucción
*(Elige un track de arriba, escúchalo activamente y anota aquí los elementos a replicar: acordes, efectos de guitarra, ritmo de batería, diseño sonoro, etc.)*

- **Track Analizado:** - **BPM Percibido:** - **Vibra/Textura:** - **Ideas para Ableton:** """

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_md)
        
        console.print(tabla)
        console.print(f"\n[bold green]¡Éxito![/bold green] Se ha generado tu nota: [bold cyan]{nombre_archivo}[/bold cyan]")
        console.print("Mueve este archivo a tu bóveda de Obsidian y ¡a producir! 🎹\n")
    except Exception as e:
        console.print(f"[bold red]Hubo un problema al guardar el archivo:[/bold red] {e}")

if __name__ == '__main__':
    generar_nota_obsidian()