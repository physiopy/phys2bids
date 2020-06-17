import sys
from distutils.dir_util import copy_tree
from os.path import join as opj
from pathlib import Path
from string import Template

from phys2bids import _version


def _save_as_html(log_path, log_content):
    """
    Save an HTML report out to a file.
    Parameters
    ----------
    body : str
        Body for HTML report with embedded figures
    """
    resource_path = Path(__file__).resolve().parent
    head_template_name = 'report_template.html'
    head_template_path = resource_path.joinpath(head_template_name)
    with open(str(head_template_path), 'r') as head_file:
        head_tpl = Template(head_file.read())

    html = head_tpl.substitute(version=_version.get_versions()['version'], log_path=log_path,
                               log_content=log_content)
    return html


def generate_report(out_dir, log_path):

    # Copy assets into output folder
    pkgdir = sys.modules['phys2bids'].__path__[0]
    assets_path = opj(pkgdir, 'reporting/assets')
    copy_tree(assets_path, f'{out_dir}/assets')

    # Read log
    with open(log_path, 'r+') as f:
        log_content = f.read()

    log_content = log_content.replace('\n', '<br>')

    html = _save_as_html(log_path, log_content)

    with open(opj(out_dir, 'phys2bids_report.html'), 'wb') as f:
        f.write(html.encode('utf-8'))
