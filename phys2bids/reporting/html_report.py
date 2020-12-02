"""Reporting functionality for phys2bids."""
import sys
from distutils.dir_util import copy_tree
from os.path import join as opj
from pathlib import Path
from string import Template
#from bokeh.models import HoverTool
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.layouts import gridplot

from phys2bids import _version


def _save_as_html(log_html_path, log_content, qc_html_path):
    """
    Save an HTML report out to a file.

    Parameters
    ----------
    body : str
        Body for HTML report with embedded figures
    """
    resource_path = Path(__file__).resolve().parent
    head_template_name = 'report_log_template.html'
    head_template_path = resource_path.joinpath(head_template_name)
    with open(str(head_template_path), 'r') as head_file:
        head_tpl = Template(head_file.read())

    html = head_tpl.substitute(version=_version.get_versions()['version'],
                               log_html_path=log_html_path, log_content=log_content,
                               qc_html_path=qc_html_path)
    return html


def _update_fpage_template(tree_string, bokeh_id, bokeh_js, log_html_path, qc_html_path):
    """
    Populate a report with content.

    Parameters
    ----------
    bokeh_id : str
        HTML div created by bokeh.embed.components
    about : str
        Reporting information for a given run
    bokeh_js : str
        Javascript created by bokeh.embed.components
    Returns
    -------
    HTMLReport : an instance of a populated HTML report
    """
    resource_path = Path(__file__).resolve().parent

    body_template_name = 'report_plots_template.html'
    body_template_path = resource_path.joinpath(body_template_name)
    with open(str(body_template_path), 'r') as body_file:
        body_tpl = Template(body_file.read())
    body = body_tpl.substitute(tree=tree_string,
                               content=bokeh_id,
                               javascript=bokeh_js,
                               version=_version.get_versions()['version'],
                               log_html_path=log_html_path,
                               qc_html_path=qc_html_path)
    return body


def _generate_file_tree(out_dir):
    """
    Populate a report with content.

    Parameters
    ----------
    bokeh_id : str
        HTML div created by bokeh.embed.components
    about : str
        Reporting information for a given run
    bokeh_js : str
        Javascript created by bokeh.embed.components
    Returns
    -------
    HTMLReport : an instance of a populated HTML report
    """
    # prefix components:
    space = '&emsp;'
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    def tree(dir_path: Path, prefix: str = ''):
        """Generate tree structure.

        Given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters

        from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
        """
        contents = list(dir_path.iterdir())
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():  # extend the prefix and recurse:
                extension = branch if pointer == tee else space
                # i.e. space because last, └── , above so no more |
                yield from tree(path, prefix=prefix + extension)

    tree_string = ''
    for line in tree(Path(out_dir)):
        tree_string += line + '<br>'
    return tree_string


def _generate_bokeh_plots(ch_name, timeseries, units, freq, size=(250, 500)):
    """
    Plot all the channels for visualizations as linked line plots for dynamic report.

    Parameters
    ----------
    ch_name: (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    timeseries: (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first, trigger the second.
        Contains all the timeseries recorded.
    units: (ch) list of strings
        List of the units of the channels.
    freq: (ch) list of floats
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
    figsize: tuple
        Size of the figure expressed as (size_x, size_y),
        Default is 250x750px
    -----
    outcome:
        Creates new plot with path specified in outfile.

    See Also
    --------
    https://phys2bids.readthedocs.io/en/latest/howto.html
    """
    colors = ['#ff7a3c', '#008eba', '#ff96d3', '#3c376b', '#ffd439']

    # only plots the first 50 samples of data
    max_time = 50 * freq[0]
    max_time = int(max_time)
    time = timeseries[0]  # assumes first timeseries is time
    x = time[:max_time]
    ch_num = len(ch_name)
    if ch_num > len(colors):
        colors *= 2

    downsample = int(phys_in.freq / 100)
    plots = {}
    plot_list = []
    for row, timeser in enumerate(timeseries[1:]):
        y = timeser[:max_time]
        i = row + 1

        hovertool = HoverTool(tooltips=[(ch_name[i], '@y{0.00} ' + units[i]),
                                        ('time', '@x{0.00} s')])
        tools = ['wheel_zoom,pan,reset', hovertool]
        if i == 1:
            plots[i] = figure(plot_height=size[0], plot_width=size[1],
                              tools=tools, title=f' Channel {i}: {ch_name[i]}',
                              sizing_mode='stretch_both')
            plots[i].line(x, y, color=colors[i - 1], alpha=0.9)
        if i > 1:
            plots[i] = figure(plot_height=size[0], plot_width=size[1],
                              tools=tools, title=f' Channel {i}: {ch_name[i]}',
                              x_range=plots[1].x_range, sizing_mode='stretch_both')
            plots[i].line(x, y, color=colors[i - 1], alpha=0.9)

        plot_list.append([plots[i]])
    p = gridplot(plot_list, toolbar_location='right', plot_height=250, plot_width=750)
    script, div = components(p)
    return script, div


def generate_report(out_dir, log_path, ch_name, timeseries, units, freq):
    """
    Plot all the channels for visualizations as linked line plots for dynamic report.

    Parameters
    ----------
    out_dir : str
        File path to a completed phys2bids output directory
    ch_name: (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    timeseries: (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first, trigger the second.
        Contains all the timeseries recorded.
    units: (ch) list of strings
        List of the units of the channels.
    freq: (ch) list of floats
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
    -----
    outcome:
        Creates new plot with path specified in outfile.

    See Also
    --------
    https://phys2bids.readthedocs.io/en/latest/howto.html
    """
    # Copy assets into output folder
    pkgdir = sys.modules['phys2bids'].__path__[0]
    assets_path = opj(pkgdir, 'reporting/assets')
    copy_tree(assets_path, f'{out_dir}/assets')

    # Read log
    with open(log_path, 'r+') as f:
        log_content = f.read()

    log_content = log_content.replace('\n', '<br>')
    log_html_path = opj(out_dir, 'phys2bids_report_log.html')
    qc_html_path = opj(out_dir, 'phys2bids_report.html')

    html = _save_as_html(log_html_path, log_content, qc_html_path)

    with open(log_html_path, 'wb') as f:
        f.write(html.encode('utf-8'))

    # Read in output directory structure & create tree
    tree_string = _generate_file_tree(out_dir)
    bokeh_js, bokeh_div = _generate_bokeh_plots(ch_name, timeseries, units, freq, size=(250, 750))
    html = _update_fpage_template(tree_string, bokeh_div, bokeh_js, log_html_path, qc_html_path)

    with open(qc_html_path, 'wb') as f:
        f.write(html.encode('utf-8'))