from textnode import TextNode
import os, shutil
from blocknode import Block_Type, BlockNode, markdown_to_blocks
from pathlib import Path

def main():
    reset_public()
    static = "/home/suprlazr/workspace/github.com/SSG/static"
    public = "/home/suprlazr/workspace/github.com/SSG/public"
    # copy_static_to_public(static, public)
    from_md_in_static = "/home/suprlazr/workspace/github.com/SSG/static/content/index.md"
    template_path = "/home/suprlazr/workspace/github.com/SSG/template.html"
    dest_html_path = "/home/suprlazr/workspace/github.com/SSG/public/index.html"
    dir_path_content = "/home/suprlazr/workspace/github.com/SSG/static/content"
    dest_dir_path = "/home/suprlazr/workspace/github.com/SSG/public"
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
    
#resets public directory to maintain idempotence
def reset_public():
    os.chdir("/home/suprlazr/workspace/github.com/SSG")
    public_dir_path = "/home/suprlazr/workspace/github.com/SSG/public"
    for file in os.listdir("./public"):
        file_path = os.path.join(public_dir_path, file)
        print(file_path)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

#substitute for shutil.copytree to practice recursion with os and shutil operations
def copy_static_to_public(dir, dest):
    if os.path.isdir(dir):
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
        for file in os.listdir(dir):
            current_static = os.path.join(dir, file)
            current_public = os.path.join(dest, file)
            # file_path = os.path.join(dir, file)
            # print(current_static)
            if os.path.isdir(current_static):
                if not os.path.exists(current_public):
                    os.mkdir(current_public)
                copy_static_to_public(current_static, current_public)
            elif os.path.isfile(current_static):
                shutil.copy(current_static, current_public)
    elif os.path.isfile(dir):
        shutil.copy(dir, dest)

#read markdown file at from_path and turn it into a variable]
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        current_content = os.path.join(dir_path_content, file)
        current_dest = os.path.join(dest_dir_path, file)
        if os.path.isdir(current_content):
            if not os.path.exists(current_dest):
                os.makedirs(current_dest, exist_ok=True)
            generate_pages_recursive(current_content, template_path, current_dest)
        elif os.path.isfile(current_content):
            print(f"Generating page from {current_content} to {dest_dir_path} using {template_path}")
            find_ext = os.path.splitext(file)
            if find_ext[1] != ".md":
                shutil.copy2(current_content, current_dest)
            else:
                d_html= current_dest.replace(".md",".html")
                with open(current_content, 'r') as f:
                    md_read = f.read()
                with open(template_path) as t:
                    template_read = t.read()
                convert_md = markdown_to_blocks(md_read)
                t_edit_head = template_read
                title1_find = convert_md.find("<h1>")
                if title1_find != -1:
                    title2_find = convert_md.find("</h1>")
                    t_edit_head = template_read.replace("{{ Title }}", convert_md[title1_find+4:title2_find])
                else:
                    t_edit_head = t_edit_head.replace("{{ Title }}", "No Title")
                t_edit_content = t_edit_head.replace("{{ Content }}", convert_md)
                #open dest path to write to it, then copy Template to dest path
                with open(d_html, 'w') as d:
                    d.write(t_edit_content)
    
        
main()


