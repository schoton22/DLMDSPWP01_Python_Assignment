"""
Visualization Module
Utilizes Bokeh to create clear and interactive plots of training, ideal, and test data.
Generates a multi-plot grid to handle varying data scales.
"""

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, TeX, Legend, LegendItem
from bokeh.layouts import gridplot, column
import pandas as pd

class Visualizer:
    """
    Handles the generation of diagnostic plots.
    """
    
    def __init__(self, output_path="results_visualization.html"):
        self.output_path = output_path
        output_file(self.output_path)

    def plot_results(self, train_df, ideal_df, chosen_info, mapped_test_df):
        """
        Creates a dashboard with a 2x2 grid for training data and a plot for test data.
        """
        training_plots = []
        test_plots = []
        colors = ["blue", "orange", "green", "red"]

        legend_positions = {
            'y1': 'top_left',
            'y2': 'top_left',
            'y3': 'top_center',
            'y4': 'top_right'
        }
        
        # 1. Create a 2x2 Grid for Training vs. Ideal
        for i, col in enumerate([c for c in train_df.columns if c != 'x']):
            ideal_col = chosen_info[col]['ideal_column']
            
            # Extract numbers for LaTeX formatting
            t_num = col[1:]
            i_num = ideal_col[1:]
            train_tex = rf"Y_{{{t_num}}}"
            ideal_tex = rf"y_{{{i_num}}}"

            p = figure(x_axis_label='x', y_axis_label='y', width=450, height=300)
            p.title.text = TeX(text=rf"\text{{Training }} {train_tex} \text{{ fits Ideal }} {ideal_tex}")
            
            # Plot Training Points
            r_train = p.scatter(train_df['x'], train_df[col], color=colors[i], 
                                marker="circle")
            
            # Plot Ideal Line
            r_ideal = p.line(ideal_df['x'], ideal_df[ideal_col], color="black")
            
            legend = Legend(items=[
                LegendItem(label=train_tex, renderers=[r_train]),
                LegendItem(label=ideal_tex, renderers=[r_ideal])
            ])
            legend.location = legend_positions.get(col, "top_left")
            p.add_layout(legend)
            
            training_plots.append(p)

        # 2. Individual Test Mapping Grid (2x2)
        for i, (train_col, info) in enumerate(chosen_info.items()):
            ideal_name = info['ideal_column']
            i_num = ideal_name[1:]
            ideal_tex = rf"y_{{{i_num}}}"
            
            p = figure(x_axis_label='x', y_axis_label='y', width=450, height=300)
            p.title.text = TeX(text=rf"\text{{Test Points Mapped to }} {ideal_tex}")

            subset = mapped_test_df[mapped_test_df['ideal_function_no'] == ideal_name]
            source = ColumnDataSource(subset)
            
            p.line(ideal_df['x'], ideal_df[ideal_name], color="black", line_dash="dashed")
            
            test_scat = p.scatter('x', 'y', source=source, color=colors[i], marker="circle")
            
            p.add_tools(HoverTool(renderers=[test_scat], tooltips=[("X", "@x"), ("Y", "@y"), ("Dev", "@delta_y")]))
            
            legend = Legend(items=[
                LegendItem(label=rf"Test Point", renderers=[test_scat])
            ])
            legend.location = legend_positions.get(train_col, "top_left")
            p.add_layout(legend)
            
            test_plots.append(p)

        # 3. Full Scope Test Plot
        p_full = figure(x_axis_label='x', y_axis_label='y')
        p_full.title.text = TeX(text=r"\text{Full Scope Test Data: Mapped vs. Unmapped}")

        full_legend_items = []
        for i, (train_col, info) in enumerate(chosen_info.items()):
            ideal_name = info['ideal_column']
            i_num = ideal_name[1:]
            ideal_tex = rf"y_{{{i_num}}}"
            subset = mapped_test_df[mapped_test_df['ideal_function_no'] == ideal_name]
            
            r = p_full.scatter(subset['x'], subset['y'], marker="circle", color=colors[i])
            full_legend_items.append(LegendItem(label=rf"Mapped to {ideal_tex}", renderers=[r]))

        # Unmapped points
        unmapped = mapped_test_df[mapped_test_df['ideal_function_no'].isnull()]
        r_un = p_full.scatter(unmapped['x'], unmapped['y'], marker="x", color="black")
        full_legend_items.append(LegendItem(label="Unmapped (Outliers)", renderers=[r_un]))

        full_legend = Legend(items=full_legend_items, location="bottom_right", background_fill_alpha=0.0)
        p_full.add_layout(full_legend)
        p_full.add_tools(HoverTool(tooltips=[("X", "@x"), ("Y", "@y")]))

        # Final Layout
        layout = column(
            gridplot(training_plots, ncols=2),
            gridplot(test_plots, ncols=2),
            p_full
        )
        show(layout)