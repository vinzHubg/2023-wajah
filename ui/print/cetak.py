import os
from xhtml2pdf import pisa
from ui.print.template import get_template

pisa.showLogging()


def cetak(source_html, output_filename):
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        source_html,
        dest=result_file)
    result_file.close()

    os.startfile(output_filename.replace("/", "\\"))

    return pisa_status.err


if __name__ == "__main__":
    source_html = get_template("data_absensi.html").render()
    cetak(source_html, "report.pdf")
