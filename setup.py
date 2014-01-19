from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import subprocess
import sys

hidapi = "hidapi-libusb"

# Check for
try:
  subprocess.check_call(["pkg-config", hidapi, "--exists"])
except subprocess.CalledProcessError:
  try:
    # Called hidapi in Homebrew
    hidapi = "hidapi"
    subprocess.check_call(["pkg-config", hidapi, "--exists"])
  except subprocess.CalledProcessError:
    print("Can't find hidapi nor hidapi-libusb")
    sys.exit(1)
except OSError, msg:
  print("Error while executing pkg-config: %s" % msg)
  sys.exit(1)

flags = subprocess.check_output(["pkg-config", hidapi, "--cflags-only-I"])
include_dirs = [flag[2:] for flag in flags.split()]

flags = subprocess.check_output(["pkg-config", hidapi, "--libs-only-L"])
library_dirs = [flag[2:] for flag in flags.split()]

# Setup extention for hid
hidext = Extension("hid",
                   ["hid.pyx"],
                   include_dirs=include_dirs,
                   library_dirs=library_dirs,
                   libraries=[hidapi])

# Set rpath on Linux because hidapi-libusb is not in sysroot
if sys.platform == "linux2":
  hidext.extra_link_args=map(lambda path: "-Wl,-rpath=%s" % path, library_dirs)

setup(
  name='hidapi',
  ext_modules = cythonize([hidext])
)
