#!/usr/bin/env python

############# Required Packages ############
import matplotlib.pyplot as plt, scienceplots, matplotlib.colors as mcolors, os

############# PLOT SETTINGS ############
plot_size           = (4, 3)
colors              = ['#e41a1c', '#008000']
markers             = ['o', 's', '^', 'D', 'h']
graphic_font        = 'stixsans'
math_font           = 'stixsans'  # ['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']
spine_width         = 1
markersize          = 4
capsize             = 3
markeredgewidth     = 0.75
legend_linewidth    = 1
linewidth           = 0.5
tick_width          = 0.75
tick_length         = 4
minor_tick_width    = 0.5
minor_tick_length   = 2
tick_labelsize      = 10
legend_fontsize     = 8
legend_boxwidth     = 0.75
label_fontsize      = 12
borderaxespad       = 0.6
alpha               = 0.5
resolution_value    = 1200

############# FUNCTION TO PROCESS COLORS ############
def face_colors(colors, alpha):
    rgba_colors = [mcolors.to_rgba(c) for c in colors]
    
    return [(rgba[0], rgba[1], rgba[2], alpha) for rgba in rgba_colors]

face_colors = face_colors(colors, alpha)

############# PLOT FUNCTIONS ############
def plot_init():
    """Creates a matplotlib figure and axis with predefined styles and applies tick settings."""
    with plt.style.context(['ieee']):
        plt.rcParams['font.family'] = graphic_font
        fig, ax = plt.subplots(figsize=plot_size)

        # Set spine widths
        for spine in ax.spines.values():
            spine.set_linewidth(spine_width)

        # Apply tick parameters
        ax.tick_params(axis='both', which='major', direction='in', width=tick_width, length=tick_length,
                       labelsize=tick_labelsize, bottom=True, top=True, left=True, right=True)
        ax.tick_params(axis='both', which='minor', direction='in', width=minor_tick_width, length=minor_tick_length,
                       bottom=True, top=True, left=True, right=True)

        return fig, ax

def style_legend(ax, loc, ncol, borderaxespad, fontsize=None, boxwidth=None, edgecolor='black'):
    if fontsize is None:
        fontsize = legend_fontsize
    if boxwidth is None:
        boxwidth = legend_boxwidth

    legend = ax.legend(fontsize=fontsize, loc=loc, ncol=ncol, borderaxespad=borderaxespad)
    outline = legend.get_frame()
    outline.set_linewidth(boxwidth)
    outline.set_edgecolor(edgecolor)

    return legend

def save_figure(fig, filename):
    """Saves the figure with the predefined resolution."""
    output_dir = os.getcwd()
    file_path = os.path.join(output_dir, filename)
    fig.savefig(file_path, dpi=resolution_value, bbox_inches='tight')
    fig.savefig(fr"{filename}", dpi=resolution_value, bbox_inches='tight')

#################### END OF CODE #####################