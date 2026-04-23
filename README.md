# TP1delgoat
DIA 1 8/4
Cree el repositorio gamer
Cree toda la interfaz donde tengo botones y controles, pausa, play, stop, shuffle, next, y previous

DIA 2 9/4
le di funciones a los botones, previous, mejore el play, stop
agregue 2 playlists y sus botones q cuando clickeas aparece las canciones q incluye, bien gaming
se repoduce la musica completamente epicamente
puse 2 temazos

dias pervios al 15/4
codee en casa por los jajas y hice el volumen mejore el slider y cositas

15/4 
termine bien el slider
hice bien el shuffle el prev song y el next song

16/04
estuve batallando con yt_dlp, hay problemas de formatos, de js y otras cosas
hice el buscador con su respectivo boton pero no dan para mas jefe
cambie todo a vlc importantisimo
se me habian creado unos archivos temporales por las descargas de yt_dlp pero no me sirven asi q los borre
cree search.py, downloader.py y logre q se muestren los resultados
borre musicplayer.py porq estaba al pedo, despues lo modularizo
arranque a manejar spotiapi

21/04
PROBLEMAS, yt_dlp dice q soy un bot (nunca me vio jugando), me dice q tendria q logearme
lo arregle descargando las cookies localmente, habria q actualizarlas cada tanto pero sirve :)
mejore como busca en spotiapi y en youtube
logre mostrar metadata, epico se ve muy bien aunq se equivoca a veces y a veces no encuentra nada
se me creo un .chache q supongo q es por las cookies dps averiguo
hice posible descargar canciones con un frame escondido atras de todo q se muestra cuando queres descargar un temita
agrande el tamaño de la app por defecto para q entre este boton

22/04
iluminacion, tuve ideas, primero hice q cada cancion muestre su duracion y tenga un boton de borrar
despues agregre creacion, edicion y eliminacion de playlists. EPICO
pero mas epico como llegue a casa y se me ocurre agregar letras, entonces un boton q ejecuta una busqueda con una api llamada ovh
tambien hice el buscador de dentro de una playlist y para agregar mediante archivos de la compu
arregle un par de bugs
y despues modularice todo y lo deje listo para entregar

## Dependencias

El proyecto utiliza las siguientes librerías y módulos de Python:

### Librerías externas (requieren instalación):
- `customtkinter`: Para la interfaz gráfica moderna.
- `pillow`: Para el manejo de imágenes.
- `python-vlc`: Para la reproducción de audio/video con VLC.
- `requests`: Para hacer peticiones HTTP.
- `yt-dlp`: Para descargar y extraer información de YouTube.
- `spotipy`: Para interactuar con la API de Spotify.

### Modulos de la biblioteca estandar de Python (incluidos con Python):
- `os`: Para operaciones del sistema de archivos.
- `tkinter`: Para la interfaz gráfica básica.
- `shutil`: Para operaciones de archivos de alto nivel.
- `re`: Para expresiones regulares.
- `random`: Para generación de números aleatorios.
- `io`: Para manejo de streams de entrada/salida.

