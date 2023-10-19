import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import igraph as ig
import pickle
from UsefulPlottingFunctions.individual_info_flow_functions import *
from UsefulPlottingFunctions.addEdge import add_arrows
import plotly.figure_factory as ff

def create_network_graph(fn, var_interest, parties, arrows = False):
    '''
    Added arrows if you like.
    '''
    if type(parties[0])==dict:
        parties = set([p['value'] for p in parties])

    if 'aggregated' in fn: # aggregated network
        df, n_list, node_sizes, cmap, classification = load_individual_information_flows_pp(fn, parties)
        g, labels, node_sizes, edge_weights, node_colours, edge_colours = get_graph_attributes(df, node_sizes, classification, cmap, var_interest)
        Xn, Yn, Xe, Ye, edge_nodes = get_node_edge_positions(g)
        max_net_flow_dict, max_net_flow_target_dict = get_max_flow_dicts(df, n_list, var_interest)
        description = get_node_description(n_list, classification, max_net_flow_dict, max_net_flow_target_dict)
    
    else:
        df, n_list, node_sizes, cmap, classification = load_individual_information_flows_pp(fn, parties)
        g, labels, node_sizes, edge_weights, node_colours, edge_colours = get_graph_attributes(df, node_sizes, classification, cmap, var_interest)
        Xn, Yn, Xe, Ye, edge_nodes = get_node_edge_positions(g)
        max_net_flow_dict, max_net_flow_target_dict = get_max_flow_dicts(df, n_list, var_interest)
        description = get_node_description(n_list, classification, max_net_flow_dict, max_net_flow_target_dict)

    inv_cmap = {v: k for k, v in cmap.items()}
    # edges

    # add arrows
    edge_x_start = [x[0] for x in Xe]
    edge_x_end = [x[1] for x in Xe]
    edge_y_start = [y[0] for y in Ye]
    edge_y_end = [y[1] for y in Ye]

    edge_trace_ = []
    for i in range(len(Xe)):
        trace_ = go.Scatter(
            x=Xe[i],
            y=Ye[i],
            mode="lines",
            line=dict(width=edge_weights[i], color=edge_colours[i]),
            legendgroup = inv_cmap[edge_colours[i]],
            showlegend=False)
        
        edge_trace_.append(trace_)

    # make array of all Xn, Yn, node_sizes, node_colours, labels
    node_values = np.array([Xn, Yn, node_sizes, node_colours, labels]).T
    description
    node_trace = []
    # now plot the nodes one colour at a time
    cmap_key_list = list(cmap.keys())
    if 'agg' in fn:
        # only keep cmap values which are in the network
        # get indices of cmap values which are in the network
        cmap_indices = [i for i in range(len(cmap_key_list)) if cmap_key_list[i] in node_values[:,4]]
        for i in cmap_indices:
            # get the node values for the current colour
            node_values_i = node_values[node_values[:,3] == cmap[cmap_key_list[i]]]
            # plot the nodes
            trace_ = go.Scatter(
                x=node_values_i[:,0].astype(float),
                y=node_values_i[:,1].astype(float),
                mode="markers+text",
                # textposition="top center",
                marker=dict(size=node_values_i[:,2].astype(float), line=dict(width=1), color=node_values_i[:,3]),
                hoverinfo="text",
                name = cmap_key_list[i],
                legendgroup = cmap_key_list[i],
                hovertext=description[cmap_key_list[i]],
                text=node_values_i[:,4],
                textfont=dict(size=np.floor(node_values_i[:,2].astype(float))/5),
                showlegend=True,
            )
            node_trace.append(trace_)
    else:
        for i in range(len(cmap)):
            # get the node values for the current colour
            node_values_i = node_values[node_values[:,3] == cmap[cmap_key_list[i]]]
            des_ = [description[node] for node in node_values_i[:,4]]
            # plot the nodes
            trace_ = go.Scatter(
                x=node_values_i[:,0].astype(float),
                y=node_values_i[:,1].astype(float),
                mode="markers+text",
                # textposition="top center",
                marker=dict(size=node_values_i[:,2].astype(float), line=dict(width=1), color=node_values_i[:,3]),
                hoverinfo="text",
                name = cmap_key_list[i],
                legendgroup = cmap_key_list[i],
                hovertext=des_,
                text=node_values_i[:,4],
                textfont=dict(size=np.floor(node_values_i[:,2].astype(float))/3),
                showlegend=True,
            )
            node_trace.append(trace_)
    # nodes
    # tracer_marker = go.Scatter(
    #     x=Xn,
    #     y=Yn,
    #     mode="markers+text",
    #     textposition="top center",
    #     marker=dict(size=node_sizes, line=dict(width=1), color=node_colours),
    #     hoverinfo="text",
    #     hovertext=description,
    #     text=labels,
    #     textfont=dict(size=10),
    #     showlegend=False,
    # )


    axis_style = dict(
        title="",
        titlefont=dict(size=20),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks="",
        showticklabels=False,
    )


    layout = dict(
        # title="Information flow network",
        width=1000,
        height=1000,
        autosize=False,
        showlegend=False,
        xaxis= {'visible': False},
        # xaxis=axis_style,
        yaxis=axis_style,
        hovermode="closest",
        plot_bgcolor="#fff",
    )


    fig = go.Figure()
    if not arrows:
        for trace in edge_trace_:
            fig.add_trace(trace)

    for trace in node_trace:
        fig.add_trace(trace)

    if arrows:
        for i in range(len(edge_x_start)):
            dir_x = edge_x_end[i] - edge_x_start[i]
            dir_y = edge_y_end[i] - edge_y_start[i]
            arr_len = np.sqrt(dir_x**2 + dir_y**2)
            # normalise
            dir_x = dir_x / arr_len
            dir_y = dir_y / arr_len

            s_node = edge_nodes[i][0]
            t_node = edge_nodes[i][1]

            fig.add_annotation(dict(
                        ax=edge_x_start[i]+ dir_x *np.log(node_sizes[s_node])/30, # x start
                        ay=edge_y_start[i] + dir_y *np.log(node_sizes[s_node])/30, # y start
                        axref='x', 
                        ayref='y',
                        # make end at edge of node size
                        x=edge_x_end[i] -  dir_x *  np.log(node_sizes[t_node])/30,# - dir_x * (node_sizes[i] / 2),
                        y=edge_y_end[i] - dir_y * np.log(node_sizes[t_node])/30,#- dir_y * (node_sizes[i] / 2), 
                        xref='x', 
                        yref='y',
                        arrowwidth=0.8,#,np.max([0.1,edge_weights[i]]), # Width of arrow.
                        arrowcolor=edge_colours[i],
                        arrowsize=0.8, # (1 gives head 3 times as wide as arrow line)
                        showarrow=True, 
                        arrowhead=2,))
    # add arrows
    
    fig.update_layout(layout)

    return fig

# Create the box plot
def create_box_plot(fn, var_interest, parties):
    if 'agg' in fn:
        with open('supplementary_data/cmap.pkl', 'rb') as f:
            cmap = pickle.load(f)

        df = pd.read_csv(fn)

        # sort by median net_flow
        source_order = df.groupby('source')[var_interest].median().sort_values(ascending=False).index

        df['source_color'] = df['source'].map(cmap)
        # Create a box plot with customizations
        fig = go.Figure()

        # Create a list of unique sources sorted by increasing median
        sorted_sources = df.groupby('source')[var_interest].median().sort_values().index.tolist()

        for source in sorted_sources:
            source_data = df[df['source'] == source]
            
            # Extract outlier points and their labels
            outlier_points = []
            outlier_labels = []
            for i, row in source_data.iterrows():
                outlier_points.append(f"Information flow of {row[var_interest]}")
                outlier_labels.append(f"{row['source']} -> {row['target']}")
            
            # Create the box plot trace
            fig.add_trace(go.Box(
                y=source_data[var_interest],
                name=source,
                width=0.6,
                boxpoints='outliers',  # Show only outliers
                marker=dict(color=source_data['source_color'].iloc[0]),  # Use the source color
                text=outlier_labels,
                jitter=0.1,
                hoverinfo='text+y'
            ))

        y = var_interest.split('_')[-1]
        if y == "flow":
            y = "all years between 2013 and 2023"

        # Define layout
        fig.update_layout(
            title=f'Outgoing information flows from {y}',
            xaxis_title='source',
            yaxis_title=f'Information flow ({y})',
            showlegend=False,
            boxgap=0,  # Adjust the gap between boxes
            boxgroupgap=0,  # Adjust the gap between groups of boxes
            boxmode='group', 
            xaxis=dict(tickangle=-90),  # Rotate x tick labels by 90 degrees  # Group box plots by source
        )

        # Show the plot
        return fig

    else:
        with open('supplementary_data/cmap.pkl', 'rb') as f:
            cmap = pickle.load(f)

        df = pd.read_csv(fn)

        # filter by selected parties
        df = df[(df['source_category'].isin(parties)) & (df['target_category'].isin(parties))]

        # sort by median net_flow
        source_order = df.groupby('source')[var_interest].median().sort_values(ascending=False).index

        df['source_color'] = df['source_category'].map(cmap)
        # Create a box plot with customizations
        fig = go.Figure()

        # Create a list of unique sources sorted by increasing median
        sorted_sources = df.groupby('source')[var_interest].median().sort_values().index.tolist()

        for source in sorted_sources:
            source_data = df[df['source'] == source]
            
            # Extract outlier points and their labels
            outlier_points = []
            outlier_labels = []
            for i, row in source_data.iterrows():
                outlier_points.append(f"Information flow of {row[var_interest]}")
                outlier_labels.append(f"{row['source']} -> {row['target']}")
            
            # Create the box plot trace
            fig.add_trace(go.Box(
                y=source_data[var_interest],
                name=source,
                width=0.6,
                boxpoints='outliers',  # Show only outliers
                marker=dict(color=source_data['source_color'].iloc[0]),  # Use the source color
                text=outlier_labels,
                jitter=0.1,
                hoverinfo='text+y'
            ))

        y = var_interest.split('_')[-1]
        if y == 'flow':
            y = "all years between 2013 and 2023"

        # Define layout
        fig.update_layout(
            title=f'Outgoing information flows from {y}',
            xaxis_title='source',
            yaxis_title=f'Information flow ({y})',
            showlegend=False,
            boxgap=0,  # Adjust the gap between boxes
            boxgroupgap=0,  # Adjust the gap between groups of boxes
            boxmode='group', 
            xaxis=dict(tickangle=-90),  # Rotate x tick labels by 90 degrees  # Group box plots by source
        )

        # Show the plot
        return fig
    


# Create the box plot
def create_flow_dist_plot(fn, var_interest, parties):
    with open('supplementary_data/cmap.pkl', 'rb') as f:
        cmap = pickle.load(f)

    df = pd.read_csv(fn)

    # filter by selected parties
    df = df[(df['source_category'].isin(parties)) & (df['target_category'].isin(parties))]

    # Map party categories to colors and set up
    hist_data = [list(df[df['source_category'] == party][var_interest]) for party in df['source_category'].unique()]
    group_labels = list(df['source_category'].unique())
    c = [cmap[x] for x in group_labels]

    # Create a KDE plot
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        colors=c,
        show_hist=False  # Hide the histogram bars
    )



    # Customize the plot layout
    fig.update_layout(
        # title='Distribution of Outgoing Flows by Party (KDE Plot)',
        xaxis_title=f'Information Flow ({var_interest})',
        yaxis_title='Probability Density',
        showlegend=False,  # Show the legend to display party categories
    )
    # Show the plot
    return fig

