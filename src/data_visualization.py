import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

import matplotlib.patches as mpatches # for custom legends in the graphs

def find_number_of_rows(nr_of_axes):
    """Support function that takes the number of axis/graphs to include in the panel and 
    calculates the number of necessary rows to include in the panel with 3 columns. 
    Example: if we panel to include 8 graphs in the panel the number of rows to be 
    returned are 3 so that the panel is a 3x3 (9 total: 8 + 1 omitted).
    """
    ranges = pd.interval_range(start=0, end=60, freq=3, closed='right')

    for i, range_ in enumerate(ranges):
        if nr_of_axes in range_:
            number_of_rows = i+1

    return number_of_rows  


# Histograms panel.
def histogram_panel(
        var_list: list,
        df1: pd.core.frame.DataFrame,
        df2: pd.core.frame.DataFrame = None,
        ) -> None:
    
    number_of_graphs = len(var_list)
    rows = find_number_of_rows(number_of_graphs)
    columns = 3
    max_plots  = rows*columns

    if max_plots < number_of_graphs:
        raise Exception('Error: The number of features must fit the the number of plots in the matrix: `rows*columns >= var_list`')

    fig, ax = plt.subplots(rows, columns, figsize=(columns*3.5, rows*3.5))

    plt.suptitle(
        'Histograms',
        size=20,
        y=0.95
        )

    df1 = df1[var_list]
    
    ax = ax.reshape(-1, 1)

    for i in range(0, max_plots):
        if i < number_of_graphs:
            ax_ = ax[i, 0]
            col = df1.columns[i]
            ax_.set_title(col)
            ax_.hist(df1[col], density=True, edgecolor="black", label='Main data frame')
            if isinstance(df2, pd.core.frame.DataFrame):
                ax_.hist(df2[col], density=True, edgecolor="orange",  histtype='step', label='Alternative')
                if i == 0:
                    ax_.legend(bbox_to_anchor=(0.5, 1.4))
            ax_.grid(axis='y')
            ax_.set_axisbelow(True)
        else:
            ax_ = ax[i, 0]
            ax_.set_axis_off()

    plt.tight_layout()
    plt.show()

# Box plot panel.
def boxplot_panel(
        var_list: list,
        df1: pd.core.frame.DataFrame,
        df2: pd.core.frame.DataFrame = None,
        ) -> None:

    df1 = df1[var_list]
    # Leaving only numerical columns.
    df1 = df1[[col for col in df1.columns if pd.api.types.is_numeric_dtype(df1[col])]]

    number_of_graphs = len(df1.columns)
    rows = find_number_of_rows(number_of_graphs)
    columns = 3
    max_plots  = rows*columns
    
    if max_plots < number_of_graphs:
        raise Exception('Error: The number of features must fit the the number of plots in the matrix: `rows*columns >= total numerical columns`')

    fig, ax = plt.subplots(rows, columns, figsize=(columns*3.0, rows*4.5))


    plt.suptitle(
        'Box Plots',
        size=20,
        y=1
        )

    ax = ax.reshape(-1, 1)

    for i in range(0, max_plots):
        if i < number_of_graphs:
            ax_ = ax[i, 0]
            col = df1.columns[i]
            ax_.set_title(col)
            sns.boxplot(
                df1[col],
                width=0.5,
                color='g',
                saturation=0.6,
                medianprops={'color': 'red'},
                ax=ax_
                )
            
            if isinstance(df2, pd.core.frame.DataFrame):
                colors = ['blue', 'orange']

                sns.boxplot(
                    [df1[col], df2[col]],
                    width=0.5,
                    saturation=0.5,
                    palette=colors,
                    medianprops={'color': 'red'},
                    ax=ax_,
                    )
                
                if i == 0:
                    # Create legend patches based on the colors
                    legend_patches = [
                        mpatches.Patch(color=colors[0], label='Main data frame'),
                        mpatches.Patch(color=colors[1], label='Alternative')
                    ]

                    # Add the legend to the plot
                    ax_.legend(
                        handles=legend_patches,
                        bbox_to_anchor=(0.5, 1.4)
                        )

            ax_.set_xticklabels('')
            ax_.grid(axis='y')
            ax_.set_axisbelow(True)



        else:
            ax_ = ax[i, 0]
            ax_.set_axis_off()

    plt.tight_layout()
    plt.show()



# Correlation heatmap.
def heat_map(feats: list, df: pd.core.frame.DataFrame):
    
    corr = df[feats].corr(method='pearson', numeric_only=True)

    length = len(feats)

    if length > 30:
        raise Exception('Too many variables (over 30) betray the purpose of the heatmap that is to facilitate the detection of extreme correlations by observation.')

    size = 6 # figure size

    # Mechanism to increase the figure size proportionally to the increase of the interval the variables
    # belong to; the interval has periods of 5 variables in ends in 30.
    intervals = pd.interval_range(
        start=0, end=30, periods=5, closed='left'
        )

    for index, interval in enumerate(intervals):
        multiplier = 1.2
        if length in interval:
            size_increment = round((index)*multiplier, 2)
            size = size + size_increment

    # Draw a heatmap with the numeric values in each cell.
    fig, ax = plt.subplots(figsize=(size, size))

    plt.title("Pearson's Correlation Heatmap", size=15)

    # Getting the Upper Triangle of the co-relation matrix.
    matrix = np.triu(corr)
    annotations = [True if length <= 15 else False][0]
    print(annotations)

    sns.heatmap(corr,
                annot=annotations,
                linewidths=.5,
                mask=matrix,
                ax=ax)

    plt.tight_layout()
    plt.show()


# Scatter plots panel.
def scatterplot_panel(
    var_list: list,
    target_var: str,
    df1: pd.core.frame.DataFrame,
    df2: pd.core.frame.DataFrame = None,
    custom_title: str = None,
    ):
    """Choose a DataFrame, a list of independent variables, a target variable, and the configuration 
    of the panel: rows x columns; to produce a pre-configured panel of scatterplots.
    """
    
    target1 = df1[target_var]
    df1 = df1[var_list]
    number_of_graphs = len(var_list)
    rows = find_number_of_rows(number_of_graphs)
    columns = 3
    max_plots  = rows*columns
    
    if max_plots < number_of_graphs:
        raise Exception('Error: The number of features must fit the the number of plots in the matrix: `rows*columns >= var_list`')

    fig, ax = plt.subplots(rows, columns, figsize=(columns*3.5, rows*3.5))

    if custom_title:
        plt.suptitle(custom_title, size=20, y=1)
    else:
        plt.suptitle(f'Scatter Plots - Features Vs {target_var}', size=20, y=1)

    ax = ax.reshape(-1, 1)

    for i in range(0, max_plots):
        if i < number_of_graphs:
            ax_ = ax[i, 0]
            col = df1.columns[i]
            ax_.set_title(col)
            
            if isinstance(df2, pd.core.frame.DataFrame):
                target2 = df2[target_var]
                removed_values_index = [i for i in df1.index if i not in df2.index]
                ax_.scatter(
                    df2[col], 
                    target2,
                    c='orange',
                    label='Values kept after transformation.'
                    )
                ax_.scatter(
                    df1.loc[removed_values_index, col],
                    target1[removed_values_index],
                    c='blue',
                    label='Values removed from main data frame.'
                    )
                if i == 0:
                    ax_.legend(bbox_to_anchor=(0.5, 1.4))
            else:
                ax_.scatter(df1[col], target1)

            ax_.grid()
            ax_.set_axisbelow(True)
            
            # Rotate x tick labels if x ticks have more than 5 characters.
            x_labels = [text.get_text() for text in ax_.get_xticklabels()]
            
            if any([True for label in x_labels if len(label) > 5]):
                # ax_.set_xticklabels(x_labels, rotation = 50)
                ax_.tick_params(axis='x', labelrotation=50)

        else:
            ax_ = ax[i, 0]
            ax_.set_axis_off()

    plt.tight_layout()
    plt.show()


# Scatter plot - queried/filtered dataframes.
def scatter_compare_filtered(
    y: str,
    x: str,
    filtered_dfs: list,
    queries: list
    ):

    # plt.style.use('classic')

    colors = ['purple', 'blue', 'green', 'orange', 'black', 'yellow',]

    fig, ax = plt.subplots(figsize=(4, 4))

    plt.suptitle(f'Queried Feature: {x} Vs {y}')

    for i, df in enumerate(filtered_dfs):
        # df = filtered_dfs[i]
        ax.scatter(df[x], df[y], color=colors[i], label=queries[i])
        ax.grid()
        ax.set_axisbelow(True)

    plt.legend(bbox_to_anchor=[1.0, 1.0])
    plt.xlabel(x)
    plt.ylabel(y)
    
    # plt.tight_layout()
    plt.show()
    
    return  


# Scatter plots panel for residuals (train and test) vs target.
def resid_visual_analysis_1(
    residuals: pd.core.series.Series,
    prediction: pd.core.series.Series,
    target: str,
    df,
    residuals_set: str,
    ):

    fig, ax = plt.subplots(1, 2, figsize=(2*3.5, 1*3.5))

    plt.suptitle(
        f'Residuals: {residuals_set}',
        size=15,
        y=1
        )

    # Residuals vs target.
    ax[0].scatter(residuals, df[target])
    ax[0].set_title('Residuals Vs Target Variable')
    ax[0].set_ylabel('residuals')
    ax[0].set_xlabel(target)
    ax[0].grid()
    ax[0].set_axisbelow(True)

    # Predicted Vs Observed. 
    ax[1].scatter(prediction, df[target])
    ax[1].set_title('Predicted Vs Observed')
    ax[1].set_xlabel('Predicted')
    ax[1].set_ylabel('Observed')
    ax[1].grid()
    ax[1].set_axisbelow(True)

    plt.tight_layout()
    plt.show()


def resid_visual_analysis_2(residuals: pd.core.series.Series, target_series: pd.core.series.Series):

    # Plots for normal distribution.

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

    # ax1
    ax1.set_title('Residual Vs Predicted Values', size=15)
    ax1.scatter(target_series, residuals)
    ax1.hlines(0, xmin=target_series.min(), xmax=target_series.max(), colors='red')
    ax1.set_ylabel('Residuals')
    ax1.set_xlabel('Predicted Values')
    ax1.grid()
    ax1.set_axisbelow(True)

    # ax2
    ax2.set_title('Histogram: Distribution Of Residuals', size=15)
    sns.histplot(residuals, kde=True, color='blue', ax=ax2)
    ax2.grid()
    ax2.set_axisbelow(True)


    # ax3
    ax3.set_title('Disparity Between Residuals Quantiles And Normally Distributed Quantiles', size=15)
    sm.ProbPlot(residuals).qqplot(line='s', ax=ax3)
    ax3.grid()
    ax3.set_axisbelow(True)

    
    plt.tight_layout()
    plt.show()