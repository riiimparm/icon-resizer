#!/usr/bin/env python3
"""
icogen - macOS App Icon Generator
Generates all required icon sizes for macOS .icns from a single source image.
"""

import argparse
import sys
import os
from pathlib import Path

# macOS required icon sizes: (size, scale, filename)
MACOS_ICON_SIZES = [
    (16,   1, "icon_16x16.png"),
    (16,   2, "icon_16x16@2x.png"),
    (32,   1, "icon_32x32.png"),
    (32,   2, "icon_32x32@2x.png"),
    (128,  1, "icon_128x128.png"),
    (128,  2, "icon_128x128@2x.png"),
    (256,  1, "icon_256x256.png"),
    (256,  2, "icon_256x256@2x.png"),
    (512,  1, "icon_512x512.png"),
    (512,  2, "icon_512x512@2x.png"),
]


def check_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        print("Error: Pillow is not installed.", file=sys.stderr)
        print("Install it with: pip install Pillow", file=sys.stderr)
        sys.exit(1)


def resize_icon(src: Path, out_dir: Path, verbose: bool = False, icns: bool = False):
    Image = check_pillow()

    # Validate source
    if not src.exists():
        print(f"Error: Source file not found: {src}", file=sys.stderr)
        sys.exit(1)

    try:
        img = Image.open(src).convert("RGBA")
    except Exception as e:
        print(f"Error: Cannot open image: {e}", file=sys.stderr)
        sys.exit(1)

    w, h = img.size
    if w != h:
        print(f"Warning: Image is not square ({w}x{h}). Will be stretched.", file=sys.stderr)
    if w < 1024 or h < 1024:
        print(f"Warning: Source image is {w}x{h}. Recommended minimum is 1024x1024.", file=sys.stderr)

    # Prepare output directory (iconset folder for icns)
    if icns:
        iconset_dir = out_dir / (src.stem + ".iconset")
        iconset_dir.mkdir(parents=True, exist_ok=True)
        target_dir = iconset_dir
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        target_dir = out_dir

    generated = []

    for size, scale, filename in MACOS_ICON_SIZES:
        px = size * scale
        resized = img.resize((px, px), Image.LANCZOS)
        out_path = target_dir / filename
        resized.save(out_path, "PNG", optimize=True)
        generated.append((filename, px))
        if verbose:
            print(f"  ✓ {filename:30s} ({px}x{px}px)")

    print(f"\nGenerated {len(generated)} icons → {target_dir}")

    # Optionally build .icns with iconutil (macOS only)
    if icns:
        import platform
        if platform.system() != "Darwin":
            print("\nNote: .icns generation requires macOS (iconutil). Skipping.")
            print(f"You can run manually: iconutil -c icns \"{iconset_dir}\"")
        else:
            icns_path = out_dir / (src.stem + ".icns")
            ret = os.system(f'iconutil -c icns "{iconset_dir}" -o "{icns_path}"')
            if ret == 0:
                print(f"✓ .icns created → {icns_path}")
            else:
                print("Warning: iconutil failed. Check the .iconset folder manually.", file=sys.stderr)

    return generated


def main():
    parser = argparse.ArgumentParser(
        prog="icogen",
        description="Generate all macOS app icon sizes from a single source image.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python icogen.py icon.png
  python icogen.py icon.png -o ./MyApp.iconset
  python icogen.py icon.png --icns
  python icogen.py icon.png --icns -o ./output -v

Output filenames follow Apple's naming convention:
  icon_16x16.png, icon_16x16@2x.png, icon_32x32.png, ...
        """,
    )
    parser.add_argument("source", nargs="?", help="Source image (PNG recommended, min 1024x1024)")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory (default: ./icons/)",
    )
    parser.add_argument(
        "--icns",
        action="store_true",
        help="Also build .icns file via iconutil (macOS only)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show each generated file",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all sizes that will be generated and exit",
    )

    args = parser.parse_args()

    if args.list:
        print("macOS App Icon sizes:")
        print(f"  {'Filename':<30} {'Logical':<10} {'Actual px'}")
        print("  " + "-" * 55)
        for size, scale, fname in MACOS_ICON_SIZES:
            px = size * scale
            logical = f"{size}x{size}" + (f" @{scale}x" if scale > 1 else "")
            print(f"  {fname:<30} {logical:<10} {px}x{px}")
        print(f"\nTotal: {len(MACOS_ICON_SIZES)} files")
        sys.exit(0)

    if not args.list and not args.source:
        parser.error("source is required")

    src = Path(args.source)
    out_dir = Path(args.output) if args.output else Path("icons")

    print(f"icogen — macOS App Icon Generator")
    print(f"Source : {src}")
    print(f"Output : {out_dir}")
    if args.icns:
        print(f"Mode   : PNG + .icns")
    print()

    resize_icon(src, out_dir, verbose=args.verbose, icns=args.icns)


if __name__ == "__main__":
    main()
