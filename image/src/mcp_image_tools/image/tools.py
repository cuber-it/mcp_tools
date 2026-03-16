"""Image tool implementations — Pillow-based, no MCP dependency."""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path

from PIL import Image


def _to_base64(img: Image.Image, fmt: str = "PNG", quality: int = 85) -> str:
    """Convert PIL Image to base64 string."""
    buf = io.BytesIO()
    save_kwargs = {"format": fmt}
    if fmt.upper() in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
    if fmt.upper() == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(buf, **save_kwargs)
    return base64.b64encode(buf.getvalue()).decode()


def _resize_to_max_width(img: Image.Image, max_width: int) -> Image.Image:
    """Resize image keeping aspect ratio if wider than max_width."""
    if max_width > 0 and img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    return img


def image_read_base64(path: str, max_width: int = 0) -> str:
    """Read an image file and return as base64-encoded PNG"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {p}"
        img = Image.open(p)
        img = _resize_to_max_width(img, max_width)
        return _to_base64(img)
    except Exception as e:
        return f"Error: {e}"


def image_resize(path: str, width: int, height: int = 0) -> str:
    """Resize an image and return as base64-encoded PNG"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {p}"
        img = Image.open(p)
        if height <= 0:
            ratio = width / img.width
            height = int(img.height * ratio)
        img = img.resize((width, height), Image.LANCZOS)
        return _to_base64(img)
    except Exception as e:
        return f"Error: {e}"


def image_crop(path: str, x: int, y: int, width: int, height: int) -> str:
    """Crop a region from an image and return as base64-encoded PNG"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {p}"
        img = Image.open(p)
        cropped = img.crop((x, y, x + width, y + height))
        return _to_base64(cropped)
    except Exception as e:
        return f"Error: {e}"


def image_screenshot(region: str = "", max_width: int = 1280) -> str:
    """Take a desktop screenshot and return as base64-encoded PNG"""
    try:
        import subprocess
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            tmp = f.name

        if region:
            # region = "x,y,width,height"
            parts = [int(x.strip()) for x in region.split(",")]
            if len(parts) != 4:
                return "Error: region must be 'x,y,width,height'"
            x, y, w, h = parts
            # Try scrot (Linux)
            result = subprocess.run(
                ["scrot", "-a", f"{x},{y},{w},{h}", tmp],
                capture_output=True, text=True, timeout=10,
            )
        else:
            # Full screen
            result = subprocess.run(
                ["scrot", tmp],
                capture_output=True, text=True, timeout=10,
            )

        if result.returncode != 0:
            # Fallback: try import (ImageMagick)
            if region:
                x, y, w, h = parts
                geo = f"{w}x{h}+{x}+{y}"
                result = subprocess.run(
                    ["import", "-window", "root", "-crop", geo, tmp],
                    capture_output=True, text=True, timeout=10,
                )
            else:
                result = subprocess.run(
                    ["import", "-window", "root", tmp],
                    capture_output=True, text=True, timeout=10,
                )

        if result.returncode != 0:
            return f"Error: screenshot failed. Install scrot or imagemagick."

        img = Image.open(tmp)
        img = _resize_to_max_width(img, max_width)
        b64 = _to_base64(img)
        Path(tmp).unlink(missing_ok=True)
        return b64
    except FileNotFoundError:
        return "Error: scrot or import not found. Install: apt install scrot"
    except Exception as e:
        return f"Error: {e}"


def image_info(path: str) -> str:
    """Get image metadata (size, format, mode)"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {p}"
        img = Image.open(p)
        info = {
            "path": str(p),
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height,
            "size_bytes": p.stat().st_size,
        }
        return json.dumps(info, indent=2)
    except Exception as e:
        return f"Error: {e}"


def image_convert(path: str, format: str = "PNG", quality: int = 85) -> str:
    """Convert image format and return as base64"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: file not found: {p}"
        fmt = format.upper()
        if fmt not in ("PNG", "JPEG", "WEBP"):
            return f"Error: unsupported format: {fmt}. Use PNG, JPEG, or WEBP."
        img = Image.open(p)
        return _to_base64(img, fmt=fmt, quality=quality)
    except Exception as e:
        return f"Error: {e}"
