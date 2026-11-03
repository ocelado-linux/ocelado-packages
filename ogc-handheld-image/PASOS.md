# ogc-handheld: montar la imagen en OBS

## 1. Actualizar el pattern
Sube el nuevo `patterns-ogc-handheld.spec` (sustituye al anterior).
Cambios: el bootloader ya no va en el pattern (lo elige la imagen) y
`kernel-default` pasa a `Recommends`.

## 2. Meta del proyecto: repo de imágenes
En `home:Luthenis:ogc-handheld` → **Meta**, añade este bloque debajo del
`<repository name="openSUSE_Tumbleweed">` que ya tienes:

```xml
<repository name="images">
  <path project="home:Luthenis:ogc-handheld" repository="openSUSE_Tumbleweed"/>
  <arch>x86_64</arch>
</repository>
```

El repo `openSUSE_Tumbleweed` debería tener ya estos paths (Factory primero):

```xml
<path project="openSUSE:Factory" repository="snapshot"/>
<path project="openSUSE:Factory:NonFree" repository="standard"/>
<path project="devel:microos:yuga:stable" repository="openSUSE_Tumbleweed"/>
```

## 3. Project Config
En **Project Config** deja esto (incluye el `Prefer` que ya tenías):

```
Prefer: steamos-powerbuttond gamescope-session-plus

%if "%_repository" == "images"
Type: kiwi
Repotype: staticlinks
Patterntype: none
%endif
```

## 4. Paquete de la imagen
**Create Package** → `ogc-handheld-image` y sube:

- `ogc-handheld.kiwi`
- `config.sh`
- `disk.sh`
- `_multibuild` (crea dos builds: `Generic` y `Deck`)
- `_constraints` (pide un worker con 60 GB de disco)

En el **Meta del paquete** desactiva el repo de RPMs, que solo debe
construirse en `images`:

```xml
<package name="ogc-handheld-image" project="home:Luthenis:ogc-handheld">
  <title>ogc-handheld image</title>
  <description>SteamOS-like openSUSE Tumbleweed con kernel OGC</description>
  <build>
    <disable repository="openSUSE_Tumbleweed"/>
  </build>
</package>
```

## 5. Qué sale
En el repo `images`, por cada flavor:

- `ogc-handheld.x86_64-0.1.0-Generic-Build*.install.iso` → para la A1X
- `ogc-handheld.x86_64-0.1.0-Deck-Build*.install.iso` → para la Steam Deck

Se graba en un USB (`dd` o Fedora Media Writer). Al arrancar el USB, el
instalador pregunta en qué disco volcar el sistema; **borra ese disco
entero**. Ojo con la tarjeta SD.

## 6. Primer arranque
- Usuario: `gamer` / contraseña: `gamer`. Cámbiala con `passwd`.
- Debería entrar directo en Steam (modo juego).
- Root deshabilitado: usa `sudo` con la contraseña de `gamer`.
- Secure Boot: **desactivado** de momento.
- SELinux en modo permisivo (`enforcing=0`) hasta comprobar que todo va.

## Si falla
Pasa el log del build (o el error de "unresolvable"). Lo más probable a la
primera son elecciones del tipo "have choice for X", que se resuelven con
otra línea `Prefer:` en el Project Config, o paquetes de la Deck que no
existan ya en ningún repo.
