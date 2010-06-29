import os, virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def extend_parser(optparse_parser):
    optparse_parser.add_option("-r", "--requirement", dest="req_file",
        default=os.path.join(os.path.dirname(__file__), "requirements.txt"),
        help="Bootstrap a buildbot build environment.")

def after_install(options, home_dir):
    subprocess.call(["pip", "install", "-E", home_dir, "--requirement", options.req_file])
"""))
f = open(os.path.join('setup', 'bootstrap.py'), 'w').write(output)
