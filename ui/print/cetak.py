import os
import platform
import subprocess
from xhtml2pdf import pisa
from ui.print.template import get_template

pisa.showLogging()

def open_file(output_filename):
    system_platform = platform.system()
    if system_platform == 'Windows':
        os.startfile(output_filename.replace("/", "\\"))
    elif system_platform == 'Darwin':  # macOS
        subprocess.call(('open', output_filename))
    elif system_platform == 'Linux':
        subprocess.call(('xdg-open', output_filename))
    else:
        raise OSError(f"Unsupported operating system: {system_platform}")

def cetak(source_html, output_filename):
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        source_html,
        dest=result_file)
    result_file.close()

    open_file(output_filename)

    return pisa_status.err


if __name__ == "__main__":
    source_html = get_template("data_absensi.j2").render()
    cetak(source_html, "report.pdf")
