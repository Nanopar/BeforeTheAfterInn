import re

def fix_landscape_visibility(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Hook into orientation change & window resize without breaking JS/audio functions
    orientation_fix = """
      window.addEventListener("orientationchange", function() {
        setTimeout(function() {
          if (typeof ensureAspectRatio === "function") {
            ensureAspectRatio();
          }
        }, 200);
      });
      
      window.addEventListener("resize", function() {
        if (typeof ensureAspectRatio === "function") {
          ensureAspectRatio();
        }
      });
    """

    # Inject the event listeners safely right before the closing </script> tag
    if "</script>" in content:
        # Find the last occurrence of </script>
        idx = content.rfind("</script>")
        content = content[:idx] + orientation_fix + "\n    </script>" + content[idx + 9:]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully added orientation recovery listener!")
    else:
        print("Could not find </script> tag.")

if __name__ == "__main__":
    fix_landscape_visibility('index.html')