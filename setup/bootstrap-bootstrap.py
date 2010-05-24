import os, virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    proj_path = os.path.dirname(__file__)
    subprocess.call(["pip", "install", "-E", home_dir, "--requirement", 
        os.path.join(proj_path, "requirements.txt")])
"""))
f = open(os.path.join('setup', 'bootstrap.py'), 'w').write(output)
