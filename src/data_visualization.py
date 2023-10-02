from typing import Union

from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # for custom legends in the graphs
import seaborn as sns
import statsmodels.api as sm

from src.utils import unfold_dictionary

    
@dataclass
class Display_Panels:

    def __init__(self, ctrl_display_panels: dict, all_data_sets_: dict, split: bool,):
        self.keys = ['df', 'container', 'index', 'panel']

        # only_nones = {key: None for key in self.keys if key not in ctrl_display_panels.keys()}
        # self.full_dic = {**ctrl_display_panels, **only_nones}
        self.full_dic = unfold_dictionary(ctrl_display_panels, self.keys)
    
        self.all_data_sets = all_data_sets_
        self.split = split
        self.df_1: pd.core.frame.DataFrame = None
        self.df_2_hist: pd.core.frame.DataFrame = None
        self.df_2_box: pd.core.frame.DataFrame = None
        self.df_2_scatter: pd.core.frame.DataFrame = None

        if isinstance(self.full_dic['df'], (list, tuple)):
            self.df_1_hp = self.full_dic['df'][0] 
            self.df_2_hp = self.full_dic['df'][1]
        if isinstance(self.full_dic['df'], str):
            self.df_1_hp = self.full_dic['df']
            self.df_2_hp = None
        if self.full_dic['df'] is None:
            self.df_1_hp = 'train' 
            self.df_2_hp = None

        if isinstance(self.full_dic['container'], (list, tuple)):
            self.container_1_hp = self.full_dic['container'][0] 
            self.container_2_hp = self.full_dic['container'][1]
        if isinstance(self.full_dic['container'], str):
            self.container_1_hp = self.full_dic['container'] 
            self.container_2_hp = None
        if self.full_dic['container'] is None:
            self.container_1_hp = None 
            self.container_2_hp = None

        if isinstance(self.full_dic['index'], (list, tuple)):
            self.index_1_hp = self.full_dic['index'][0] 
            self.index_2_hp = self.full_dic['index'][1] 
        if isinstance(self.full_dic['index'], int):
            self.index_1_hp = self.full_dic['index'] 
            self.index_2_hp = None 
        if self.full_dic['index'] is None:
            self.index_1_hp = None 
            self.index_2_hp = None

        if isinstance(self.full_dic['panel'], (list, tuple, str)):
            self.panel_hp = self.full_dic['panel'] 
        if self.full_dic['index'] is None:
            self.panel_hp = None 

        if (self.split is False) and (self.df_1_hp == 'main'):
            self.df_1_hp = 'train' 

        if ((self.container_1_hp is None) and (self.container_2_hp is None)):
            self.full_dic['index'] == (None, None)
    
    @property
    def type_check(self,):
        if isinstance(self.full_dic['df'], str):
            if self.full_dic['df'] not in ['main', 'train']:
                raise Exception("If the main data set has not been split, `df` can only take two values: 'main' or 'train' (point to the same data set).")
            if (self.full_dic['container'] is not None) and (self.full_dic['container'] not in ['query', 'trim']):
                raise Exception("Only one data set has been selected in 'df', therefore the value in 'container' must be a string ('query' or 'trim') or `None`'")
        
        if isinstance(self.full_dic['df'], (list, tuple)):
            if len(self.full_dic['df']) != 2:
                raise Exception(f"If 'df' is a {type(self.full_dic['df'])}, it can only take two values - one for each data set.")

        if (self.full_dic['container'] is None) or ((self.container_1_hp is None) and (self.container_2_hp is None)):
            if (self.full_dic['index'] is not None) and (self.full_dic['index'] == (None, None)):
                raise Exception('No container has been selected, therefore an index cannot be passed as in input.')

        if isinstance(self.full_dic['container'], (list, tuple)):
            if len(self.full_dic['container']) != 2:
                raise Exception(f"If 'container' is a {type(self.full_dic['container'])}, it can only take two values - one for each data set.")

        if isinstance(self.full_dic['index'], (list, tuple)):
            if len(self.full_dic['index']) != 2:
                raise Exception(f"If 'index' is a {type(self.full_dic['index'])}, it can only take two values - one for each container.")

        return  

    @property
    def check_input_validity(self,):
        if (self.full_dic['container'] == 'query') or ('query' in self.full_dic['container']):
            if self.all_data_sets['query'] is None:
                raise Exception('There are no queried versions available (check the `query_container`).')

            query_container_index = list(self.all_data_sets['query'].keys())
            if (self.container_1_hp == 'query'):
                if self.index_1_hp not in query_container_index:
                    raise Exception(f'The index specified for the query container, `{self.index_1_hp}`, does not correspond to any of the elements in the `query_container`. ')
            
            if (self.container_2_hp == 'query'):
                if self.index_2_hp not in query_container_index:
                    raise Exception(f'The index specified for the query container, `{self.index_2_hp}`, does not correspond to any of the elements in the `query_container`. ')

        if (self.full_dic['container'] == 'trim') or ('trim' in self.full_dic['container']):
            if self.all_data_sets['trim'] is None:
                raise Exception('There are no trimmed versions available (check the `trim_container`).')

        # if (isinstance(self.full_dic['container'], (tuple, list))) and (isinstance(self.full_dic['index'], (tuple, list))) 

        return


    @property
    def append_data(self,) -> None:

        if self.container_1_hp is None:
            self.container_1_hp = 'processed'
            self.df_1 = self.all_data_sets[self.container_1_hp][self.df_1_hp]
        else:
            self.df_1 = self.all_data_sets[self.container_1_hp][self.index_1_hp][self.df_1_hp]
        
        if self.df_2_hp:
            if self.container_2_hp is None:
                self.container_2_hp = 'processed'
                self.df_2 = self.all_data_sets[self.container_2_hp][self.df_2_hp]
            else:
                self.df_2 = self.all_data_sets[self.container_2_hp][self.index_2_hp][self.df_2_hp]

            if ('histogram' in self.panel_hp) or (self.panel_hp == 'histogram'):
                self.df_2_hist = self.df_2
            if ('boxplot' in self.panel_hp) or (self.panel_hp == 'boxplot'):
                self.df_2_box = self.df_2
            if ('scatterplot' in self.panel_hp) or (self.panel_hp == 'scatterplot'):
                self.df_2_scatter = self.df_2   

        return 


def find_number_of_rows(nr_of_axes: str) -> str:
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

class Histogram:
    keys = ['var_list', 'bins_input', 'density_input', 'cumulative_input', 'df1', 'df2']

    def histogram_panel(
            var_list: list,
            bins_input: Union[int, dict],
            density_input: Union[str, dict],
            cumulative_input: Union[str, dict],
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
            y=1.01
            )

        df1 = df1[var_list]
        
        ax = ax.reshape(-1, 1)

        for i in range(0, max_plots):
            if i < number_of_graphs:
                ax_ = ax[i, 0]
                col = df1.columns[i]
                ax_.set_title(col)

                bins_ = 10
                density_ = False
                cumulative_ = False

                if bins_input is not None:
                    if isinstance(bins_input, int):
                        bins_ = bins_input
                    
                    if isinstance(bins_input, dict):
                        if col in bins_input:   
                            bins_ = bins_input[col]

                if density_input is not None:
                    if isinstance(density_input, bool):
                        density_ = density_input
                    if isinstance(density_input, dict):
                        if col in density_input:
                            density_ = density_input[col]

                if cumulative_input is not None:
                    if isinstance(cumulative_input, bool):
                        cumulative_ = cumulative_input
                    if isinstance(cumulative_input, dict):
                        if col in cumulative_input:
                            cumulative_ = cumulative_input[col]

                ax_.hist(
                    df1[col],
                    edgecolor="black",
                    label='Main data frame',
                    density=density_,
                    bins=bins_,
                    cumulative=cumulative_,
                    )
                if isinstance(df2, pd.core.frame.DataFrame):
                    ax_.hist(
                        df2[col], 
                        edgecolor="orange", 
                        histtype='step',
                        linewidth=3,
                        label='Alternative',
                        density=density_,
                        bins=bins_,
                        cumulative=cumulative_,
                        )
                    if i == 0:
                        ax_.legend(bbox_to_anchor=(0.5, 1.4))
                ax_.grid(axis='y')
                ax_.set_axisbelow(True)
            else:
                ax_ = ax[i, 0]
                ax_.set_axis_off()

        plt.tight_layout()
        plt.show()

        return

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

    return


def scatterplot_panel(
    var_list: list,
    target_var: str,
    df1: pd.core.frame.DataFrame,
    df2: pd.core.frame.DataFrame = None,
    custom_title: str = None,
    ) -> None:
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

    return


class Heat_Map:
    def __init__(self, heatmap_hyperparameters: dict, split):
        self.keys = ['df', 'variables']
        full_dic = unfold_dictionary(heatmap_hyperparameters, self.keys)
        self.split = split
        self.variables_hp = full_dic['variables']
        
        if full_dic['df'] is None: 
            self.df_hp = 'train'
        else:
            self.df_hp = full_dic['df']

    def display_heat_map(self, data_sets: dict) -> None:

        if self.split:
            df = data_sets[self.df_hp]
        else:
            df = data_sets[self.df_hp]

        corr = df[self.variables_hp].corr(method='pearson', numeric_only=True)

        length = len(self.variables_hp)

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

        sns.heatmap(corr,
                    annot=annotations,
                    linewidths=.5,
                    mask=matrix,
                    ax=ax)

        plt.tight_layout()
        plt.show()

        return



# Scatter plot - queried/filtered dataframes.
class Scatterplot_Comparison:
    keys = ['df', 'container', 'index', 'x', 'y',]

    def scatterplot_comparison(
        self,
        df: str,    
        y: str,
        x: str,
        filtered_sets: list,
        container: list,
        container_type: str, 
        ) -> None:

        colors = ['purple', 'blue', 'green', 'orange', 'black', 'yellow', 'red', 'brown']

        if len(filtered_sets) > len(colors):
            raise Exception('There are more arrays to fit in the scatterplot than colors to represent them.')

        fig, ax = plt.subplots(figsize=(4, 4))

        plt.suptitle(f'Queried Feature: {x} Vs {y} ({df} set)')

        for i, df in enumerate(filtered_sets):
            # df = filtered_dfs[i]

            condition = container[i]
            
            if container_type == 'trim':
                label_ = ', '.join([f'{key}: {condition[key]}' for key in condition][1:])
            if container_type == 'query':
                label_ = condition
            
            ax.scatter(df[x], df[y], color=colors[i], label=label_)
            ax.grid()
            ax.set_axisbelow(True)

        # plt.tight_layout()
        plt.legend(loc='upper center', bbox_to_anchor=[0.2, -0.2])
        plt.xlabel(x)
        plt.ylabel(y)
        
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