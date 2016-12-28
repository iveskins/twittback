import sys
import path
import subprocess


def run_sphinx(builder):
    doc_output = path.Path("doc/build").joinpath(builder)
    cmd = [
        "sphinx-build",
        "-b", builder,
        "-d", "doc/build/doctrees",
        "-W",  # treat warnings as errors
        "doc/source",
        doc_output,
    ]
    rc = subprocess.call(cmd)
    return rc, doc_output


def main():
    print("Spell checking documentation")
    _, spell_out_dir = run_sphinx("spelling")
    spell_out = spell_out_dir.joinpath("output.txt").text()
    if spell_out:
        print(spell_out, end="")
        sys.exit(1)
    else:
        print("Spell check OK")
    print("Building HTML documentation")
    rc, html_out = run_sphinx("html")
    if rc != 0:
        sys.exit(rc)
    index_html = html_out.joinpath("index.html")
    print("Doc generated in", index_html)


if __name__ == "__main__":
    main()
