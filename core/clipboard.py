import os
import shutil
import subprocess
import pyperclip


def copy_to_clipboard(text: str) -> tuple[bool, str]:
    """Menyalin teks ke clipboard Linux (mendukung Wayland & X11)."""
    if not text:
        return False, "Teks kosong, tidak ada yang disalin."

    encoded = text.encode("utf-8")

    # 1. Prioritas Wayland (wl-copy)
    if os.environ.get("WAYLAND_DISPLAY") and shutil.which("wl-copy"):
        try:
            subprocess.run(["wl-copy"], input=encoded, check=True)
            return True, "wl-copy (Wayland)"
        except subprocess.SubprocessError:
            pass

    # 2. Prioritas X11 (xclip / xsel)
    if shutil.which("xclip"):
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=encoded,
                check=True,
            )
            return True, "xclip (X11)"
        except subprocess.SubprocessError:
            pass

    if shutil.which("xsel"):
        try:
            subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=encoded,
                check=True,
            )
            return True, "xsel (X11)"
        except subprocess.SubprocessError:
            pass

    # 3. Fallback ke pyperclip
    try:
        pyperclip.copy(text)
        return True, "pyperclip"
    except pyperclip.PyperclipException:
        return (
            False,
            "Utility clipboard tidak ditemukan. Instal 'wl-clipboard' atau 'xclip'.",
        )
