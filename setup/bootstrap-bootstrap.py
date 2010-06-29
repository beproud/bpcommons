import os, virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess

def extend_parser(optparse_parser):
    optparse_parser.add_option("-b", "--buildbot", dest="buildbot", action="store_true",
        default=False, help="Bootstrap a buildbot build environment.")
    optparse_parser.add_option("-a", "--all-requirements", dest="allreqs", action="store_true",
        default=False, help="Install all requirements.")

def after_install(options, home_dir):
    proj_path = os.path.dirname(__file__)
    if options.buildbot:
        req_file = "requirements_buildbot.txt"
    elif options.allreqs:
        req_file = "requirements_all.txt"
    else:
        req_file = "requirements.txt" 
    subprocess.call(["pip", "install", "-E", home_dir, "--requirement", 
        os.path.join(proj_path, req_file)])
"""))
f = open(os.path.join('setup', 'bootstrap.py'), 'w').write(output)
