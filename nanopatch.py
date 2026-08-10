import re

def fix_canvas_stretch(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Disable GM's forced aspect ratio calculation
    content = re.sub(
        r'const\s+CHANGE_ASPECT_RATIO\s*=\s*true\s*;',
        'const CHANGE_ASPECT_RATIO = false;',
        content
    )

    # 2. Inject CSS rules to force the canvas element to fill the viewport 100%
    css_fix = """
      canvas.emscripten {
        width: 100vw !important;
        height: 100vh !important;
        max-width: 100vw !important;
        max-height: 100vh !important;
        object-fit: fill;
    """
    
    content = content.replace('canvas.emscripten {', css_fix, 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Patched canvas styling and disabled aspect ratio lock!")

if __name__ == "__main__":
    fix_canvas_stretch('index.html')