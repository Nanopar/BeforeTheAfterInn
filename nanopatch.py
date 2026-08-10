import re

def fix_gx_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find and update only the ResizeObserver block to handle orientation recovery smoothly
    old_observer = re.search(r'const resizeObserver = new ResizeObserver\(.+?\);\s*resizeObserver\.observe\(.+?\);', html_content, re.DOTALL)
    
    new_observer = """const resizeObserver = new ResizeObserver(() => {
        window.requestAnimationFrame(ensureAspectRatio);
        setTimeout(() => window.requestAnimationFrame(ensureAspectRatio), 100);
      });
      resizeObserver.observe(document.body);"""

    if old_observer:
        html_content = html_content.replace(old_observer.group(0), new_observer)
        print("Successfully patched resize observer!")
    else:
        print("Could not find resizeObserver block.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

fix_gx_html('index.html')