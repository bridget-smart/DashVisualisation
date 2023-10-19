import pandas as pd
import numpy as np
import igraph as ig
import pickle

def load_individual_information_flows_pp(fn, parties):
    """
    Function to load in the individual information flows data and get all corresponding supplementary data
    """
    # load in sample data
    df = pd.read_csv(fn)

    if 'aggregated' in fn:
        # dictionary which has the node sizes
        df = df[(df['source'].isin(parties)) & (df['target'].isin(parties))]

        n_list = set(list(df['source'].unique())+list(df['target'].unique()))


        # node size dictionary
        with open('supplementary_data/node_sizes_agg.pkl', 'rb') as f:
            node_sizes = pickle.load(f)

        # colour map for each source/target classification
        with open('supplementary_data/cmap.pkl', 'rb') as f:
            cmap = pickle.load(f)

        # dict from source / target to classification
        classification = None

    else:
        # filter by selected parties
        df = df[(df['source_category'].isin(parties)) & (df['target_category'].isin(parties))]

        # dictionary which has the node sizes
        n_list = set(list(df['source'].unique())+list(df['target'].unique()))

        # node size dictionary
        with open('supplementary_data/node_sizes.pkl', 'rb') as f:
            node_sizes = pickle.load(f)

        # colour map for each source/target classification
        with open('supplementary_data/cmap.pkl', 'rb') as f:
            cmap = pickle.load(f)

        # dict from source / target to classification
        classification = {x : y for x, y in zip(df['source'], df['source_category'])}
        classification.update({x : y for x, y in zip(df['target'], df['target_category'])})

    return df, n_list, node_sizes, cmap, classification
    
def get_max_flow_dicts(df, n_list, var_interest):
    """
    Get the maximum net flow for each source and the corresponding target
    """

    # get the maximum net flow for each source and the corresponding target
    max_net_flow = df.groupby('source')[var_interest].max().reset_index()
    max_net_flow = max_net_flow.merge(df, on=['source', var_interest], how='left')
    max_net_flow = max_net_flow[['source', 'target', var_interest]]

    # make into a dictionary
    max_net_flow_dict = {r[1]['source']:r[1][var_interest] for r in max_net_flow.iterrows()}
    max_net_flow_target_dict = {r[1]['source']:r[1]['target'] for r in max_net_flow.iterrows()}


    # add any nodes which are not in the max_net_flow_dict
    missing = set(n_list) - set(max_net_flow_dict.keys())
    for m in missing:
        # update the max_net_flow_dict
        max_net_flow_dict[m] = 0
        max_net_flow_target_dict[m] = 'None'

    return max_net_flow_dict, max_net_flow_target_dict

def get_node_description(n_list, classification, max_net_flow_dict, max_net_flow_target_dict):
    if classification == None:
        
        # create tooltip string by concatenating statistics
        description = {node:
            f"<b>{node}</b>"
            + "<br>"
            + "<br>"
            + f"Party: {node}"
            + "<br>"
            + "<br>"
            + f"Strongest information flow of {str(max_net_flow_dict[node])} <br> with: {max_net_flow_target_dict[node]}."
            for node in n_list
        }

    else:
        # create tooltip string by concatenating statistics
        description = {node:
            f"<b>{node}</b>"
            + "<br>"
            + "<br>"
            + f"Party: {classification[node]}"
            + "<br>"
            + "<br>"
            + f"Strongest information flow of {str(max_net_flow_dict[node])} <br> with: {max_net_flow_target_dict[node]}."
            for node in n_list
        }

    return description

def get_node_edge_positions(g):
    """
    Function to get the positions of the nodes and edges from graph g
    """
    # get positions, sizes, and labels
    pos = g.layout_fruchterman_reingold(weights=g.es()['weight'])
    Xn=[pos[k][0] for k in range(len(pos))]
    Yn=[pos[k][1] for k in range(len(pos))]

    # get edge positions
    Xe=[]
    Ye=[]
    Edge_nodes = []
    for e in g.es():
        Xe.append([pos[e.tuple[0]][0],pos[e.tuple[1]][0]])
        Ye.append([pos[e.tuple[0]][1],pos[e.tuple[1]][1]])
        Edge_nodes.append([e.source, e.target])

    return Xn, Yn, Xe, Ye, Edge_nodes

def get_graph_attributes(df, node_sizes, classification, cmap, var_interest):

    # non aggregated network
    if classification != None:
        g = ig.Graph.TupleList(pd.DataFrame(df[['source','target',var_interest]]).reset_index(drop=True).itertuples(index=False), directed=True, weights=True)

        # colour by category
        for vertex in g.vs():
            try:
                vertex['color'] = cmap[classification[vertex['name']]]
                vertex['size'] = node_sizes[vertex['name']]
            except:
                vertex['color'] = 'gray' # seems to happen for a few w/o any tweets? need to look into
                vertex['size'] = 1

        # edge colours
        edge_colours=[]
        for x in g.es():
            try:
                edge_colours.append(cmap[classification[g.vs()[x.source]['name']]])
            except:
                edge_colours.append('gray')

        labels = [x['name'] for x in g.vs()]
        node_sizes = [node_sizes[x] for x in labels]
        edge_weights = [float(x['weight']) for x in g.es()]
        node_colours = [x['color'] for x in g.vs()]

        return g, labels, node_sizes, edge_weights, node_colours, edge_colours
    
    else:
        g = ig.Graph.TupleList(pd.DataFrame(df[['source','target',var_interest]]).reset_index(drop=True).itertuples(index=False), directed=True, weights=True)

        # colour by category
        for vertex in g.vs():
            try:
                vertex['color'] = cmap[vertex['name']]
                vertex['size'] = node_sizes[vertex['name']]
            except:
                vertex['color'] = 'gray' # seems to happen for a few w/o any tweets? need to look into
                vertex['size'] = 1

        # edge colours
        edge_colours=[]
        for x in g.es():
            try:
                edge_colours.append(cmap[g.vs()[x.source]['name']])
            except:
                edge_colours.append('gray')

        labels = [x['name'] for x in g.vs()]
        node_sizes = [20*node_sizes[x] for x in labels]
        edge_weights = [20*float(x['weight']) for x in g.es()]
        node_colours = [x['color'] for x in g.vs()]

        return g, labels, node_sizes, edge_weights, node_colours, edge_colours
