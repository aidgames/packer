import os
import zipfile
from base64 import b64encode

TEMPLATE="""#!/usr/bin/python3
import zipfile, os, shutil, tempfile, sys, json
from io import BytesIO
from time import sleep
from base64 import b64decodedata='{}'
tempdir=tempfile.mkdtemp()
curr_dir=os.getcwd()
with zipfile.ZipFile(BytesIO(b64decode(data.encode())), "r") as zipf:
    zipf.extractall(tempdir)
data=json.load(open(tempdir+"/manifest.json"))
if os.name not in data["run"]:
    print("This is unsupported on your platform")
    sys.exit(1)
os.chdir(tempdir)
os.system(data["run"][os.name]+" "+" ".join(sys.argv[1:]))
os.chdir(curr_dir)
try:
    shutil.rmtree(tempdir)
except:
    pass
"""

TEMPLATE_COMPRESSED="""exec(__import__('base64').b64decode({}).decode())"""

def zipdir(directory, filename):
    """Zip directory"""
    with zipfile.ZipFile(f"{filename}", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root,file),os.path.relpath(os.path.join(file), os.path.join(directory, '..')))
    return filename

def ziptob64(fromfile, tofile):
    """convert zip to base64"""
    with open(fromfile, "rb") as from_file:
        with open(tofile, "wb") as to_file:
            to_file.write(b64encode(from_file.read()))

def genunpackfile(unpackfile, zipb64):
    """generate unpack.py"""
    b64data=""
    with open(zipb64, "r") as f:
        b64data=f.read()
    data=TEMPLATE.format(b64data)
    with open(unpackfile, "w+") as f:
        f.write(data)

def gencompressedunpackfile(compressedunpackfile, unpackfile):
     """compress unpack.py"""
    with open(unpackfile, "r") as f:
        with open(compressedunpackfile, "w") as cf:
            cf.write(TEMPLATE_COMPRESSED.format(b64encode(f.read().encode())))
