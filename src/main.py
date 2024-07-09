from textnode import TextNode
import os, shutil



def main():
    reset_public()
    from_path = "/home/suprlazr/workspace/github.com/SSG/static"
    dest_path = "/home/suprlazr/workspace/github.com/SSG/public"
    copy_static_to_public(from_path, dest_path)

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
        print(current_static)
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
    
        
main()


