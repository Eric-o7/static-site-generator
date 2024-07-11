from textnode import TextNode
import os, shutil
from blocknode import Block_Type, BlockNode, markdown_to_blocks


def main():
    reset_public()
    static = "/home/suprlazr/workspace/github.com/SSG/static"
    public = "/home/suprlazr/workspace/github.com/SSG/public"
    # copy_static_to_public(static, public)
    from_md_in_static = "/home/suprlazr/workspace/github.com/SSG/static/content/index.md"
    template_path = "/home/suprlazr/workspace/github.com/SSG/template.html"
    dest_html_path = "/home/suprlazr/workspace/github.com/SSG/public/index.html"
    dir_path_content = "/home/suprlazr/workspace/github.com/SSG/static"
    dest_dir_path = "/home/suprlazr/workspace/github.com/SSG/public"
    # generate_page(from_md_in_static, template_path, dest_html_path)
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
    for file in os.listdir(dir):
        current_static = os.path.join(dir, file)
        current_public = os.path.join(dest, file)
        # file_path = os.path.join(dir, file)
        # print(current_static)
        if os.path.isdir(current_static):
            os.mkdir(current_public)
            copy_static_to_public(current_static, current_public)
        elif os.path.isfile(current_static):
            shutil.copy(current_static, current_public)

#read markdown file at from_path and turn it into a variable
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_read = f.read()
    with open(template_path) as t:
        template_read = t.read()
    convert_md = markdown_to_blocks(md_read)
    title1_find = convert_md.find("<h1>")
    if convert_md.find("<h1>") != -1:
        title2_find = convert_md.find("</h1>")
        t_edit_head = template_read.replace("{{ Title }}", convert_md[title1_find+4:title2_find])
    t_edit_cont = t_edit_head.replace("{{ Content }}", convert_md)
    #open dest path to write to it, then copy Template to dest path
    with open(dest_path, 'w') as d:
        d.write(t_edit_cont)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        current_content = os.path.join(dir_path_content, file)
        current_dest = os.path.join(dest_dir_path, file)
        if os.path.isdir(current_content):
            generate_pages_recursive(current_content, template_path, current_dest)
        elif os.path.isfile(current_content):
            print(f"Generating page from {current_content} to {dest_dir_path} using {template_path}")
            find_ext = os.path.splitext(file)
            if find_ext[1] != ".md":
                shutil.copy(current_content, current_dest)
            else:
                with open(current_content) as f:
                    md_read = f.read()
                with open(template_path) as t:
                    template_read = t.read()
                convert_md = markdown_to_blocks(md_read)
                title1_find = convert_md.find("<h1>")
                if convert_md.find("<h1>") != -1:
                    title2_find = convert_md.find("</h1>")
                    t_edit_head = template_read.replace("{{ Title }}", convert_md[title1_find+4:title2_find])
                t_edit_cont = t_edit_head.replace("{{ Content }}", convert_md)
                #open dest path to write to it, then copy Template to dest path
                with open(current_dest, 'w') as d:
                    d.write(t_edit_cont)
        
main()


