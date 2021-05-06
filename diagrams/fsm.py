from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import General
from diagrams import Cluster, Diagram, Edge


# states
initial_state = "IS"
waiting_node = "WN"
reading_node = "RN"
reading_attr_name = "RAN"
reading_attr_values = "RAVs"
reading_attr_value = "RAV"

# action
init_node = "init_node"
init_attr = "init_attr"
init_attrs = "init_attrs"
copy_char = "copy_char"
copy_node_name = "copy_node_name"
copy_attr_name = "copy_attr_name"
copy_attr_val = "copy_attr_val"
init_attr_vals = "init_attr_vals"
default = "default"
name = "name"
attrs = "attrs"

# labels used during diagram creation
resource = "Resource"
s3 = "s3"
dynamo = "dynamo"
readby = "ReadBy"
writtenby = "WrittenBy"

def ignore():
    pass

def error():
    raise Exception("invalid state")

transitions = {
    initial_state: {
        "#": (waiting_node, ignore),
        "*": (reading_attr_name, init_attr),
        default: (initial_state, ignore)
    },
    waiting_node: {
        "#": (reading_node, init_node),
        default: (initial_state, ignore),
    },
    reading_node: {
        " ": (reading_node, ignore),
        '\n': (initial_state, copy_node_name),
        default: (reading_node, copy_char)
    },
    reading_attr_name: {
        '\n': (initial_state, error),
        ':': (reading_attr_values, copy_attr_name),
        default: (reading_attr_name, copy_char)
    },
    reading_attr_values: {
        '\n': (initial_state, copy_attr_val),
        default: (reading_attr_values, copy_char)
    }
}

def next_state(state, ch):
    if ch in transitions[state]:
        return transitions[state][ch]
    # if there isn't a defined transition, use the default
    return transitions[state][default]


def parse_nodes(file):
    import os
    print(os.getcwd())

    data = open(file).read()
    nodes = []
    node = None
    attr_index = -1
    curr_str = ""
    curr_attr = None
    state = initial_state
    for ch in data:

        state, action = next_state(state, ch)

        if action == ignore:
            continue
        if action == init_node:
            # if there was a previous node, add it to the list
            if node != None:
                nodes.append(node)
            node = {name: "", attrs: {}}
            attr_index = -1
        if action == copy_node_name:
            node[name] = curr_str.strip()
            curr_str = ""
        if action == copy_attr_name:
            curr_attr = curr_str.strip()
            curr_str = ""
        if action == copy_attr_val:
            node[attrs][curr_attr] = curr_str.strip()
            curr_str = ""
        if action == copy_char:
            curr_str += ch
    return nodes

def init_diagram_resources(nodes, env):
    resources = {}
    for node in nodes:
        if resource not in node[attrs] or env not in node[name]:
            print("skipping node %s because it's an empty resource" % (node[name]))
            continue

        # create the resource itself
        if node[attrs][resource] == s3:
            resources[node[name]] = S3(node[name])
        if node[attrs][resource] == dynamo:
            resources[node[name]] = Dynamodb(node[name])

        # create the processes that read / write the resource
        for proc in node[attrs][readby].split(",") + node[attrs][writtenby].split(","):
            if proc not in resources:
                resources[proc] = General(proc)

    return resources


def create_edges(nodes, resources):
    for node in nodes:
        if resource not in node[attrs]:
            print("skipping node %s because it's an empty resource" % (node[name]))
            continue

        # create the read by edges
        for proc in node[attrs][readby].split(","):
            resources[proc] >> resources[node[name]]

        for proc in node[attrs][writtenby].split(","):
            resources[proc] << resources[node[name]]
       

nodes = parse_nodes('./data-flow.md')

with Diagram("Data flows", show=False):
    with Cluster("staging"):
        staging_resources = init_diagram_resources(nodes=nodes, env="staging")
    with Cluster("production"):
        production_resources = init_diagram_resources(nodes=nodes, env="production")
    
    resources = {}
    resources.update(staging_resources)
    resources.update(production_resources)
    create_edges(nodes=nodes, resources=resources)

print('diagram done')
