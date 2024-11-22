import os
from pathlib import Path
from block_markdown import markdown_to_html_node

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        f.close()

    with open(template_path, 'r', encoding='utf-8') as f:
        updated_html = f.read()
        updated_html = updated_html.replace('{{ Title }}', str(title))
        updated_html = updated_html.replace('{{ Content }}', str(content))
        f.close()
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)
        f.write(updated_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)