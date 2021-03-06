import copy
import pathlib

import pywintypes
from win32com import client as win32

from anytree import Node, RenderTree, PostOrderIter
from anytree.exporter import DictExporter
from anytree.importer import DictImporter

from gui.models.aspen_var_catalogue import (
    BLOCKS_CATALOGUE, DESPEC_CATALOGUE, STREAMS_CATALOGUE)


# ---------------------------- ASPEN PLUS SECTION ----------------------------
class AspenConnection:
    """Aspen Plus connection class that handles JSON compatible tree
    generation.

    Parameters
    ----------
    file_path : str
        Full path string to the .bkp or .inp file.

    Notes
    -----
        Explicitly call the close_connection() function to destroy the
        connection!
    """

    # ------------------------------ CONSTANTS -------------------------------
    # CLASS
    _NODE_PATH_FORMAT = r'\Data\{0}\{1}\{2}\{3}'

    # ASPEN PLUS AttibuteValue ARGUMENTS
    _HAP_HASCHILDREN = 38  # Does this directory actually have any children?
    _HAP_PROMPT = 19  # A descriptive prompt for the node.
    _HAP_RECORDTYPE = 6  # If the node contains record, the type of that record
    _HAP_BASIS = 13  # The basis for the value attribute
    _HAP_VALUE = 0  # The value of the node
    _HAP_VALUEDEFAULT = 10  # The default value for the value attribute
    _HAP_ENTERABLE = 7  # Can the value attribute be modified?

    def __init__(self, file_path: str):
        if pathlib.Path(file_path).is_file:
            self._aspen_filepath = file_path
        else:
            raise FileNotFoundError("Couldn't find the specified .bkp file.")

        self._aspen = None

    # --------------------------- PRIVATE FUNCTIONS --------------------------
    def _check_simulation_results(self) -> None:
        """Check if the simulation has results. If not, run it so we can access
        the output nodes.
        """
        if self._aspen is None:
            self.open_connection()

        UOSSTAT2_node = self._aspen.Tree.FindNode(
            r"\Data\Results Summary\Run-Status\Output\UOSSTAT2")
        try:
            d_val = UOSSTAT2_node.Value
        except (pywintypes.com_error, AttributeError):
            # UOSSTAT2 node not built, that means the simulation has
            # no results.
            self._aspen.Engine.Run2()
            UOSSTAT2_node = self._aspen.Tree.FindNode(
                r"\Data\Results Summary\Run-Status\Output\UOSSTAT2")
        finally:
            if UOSSTAT2_node.Value is None:
                # UOSSTAT2 node is built, but its Value is None, that means
                # the simulation hasn't output data.
                self._aspen.Engine.Run2()

    def _isleaf(self, node: win32.CDispatch) -> bool:
        """Check if node is leaf or branch.

        Parameters
        ----------
        node : win32.CDispatch
            Node to be checked.

        Returns
        -------
        bool
            Whether the node is a leaf (True) or not (False).
        """
        if node.AttributeValue(self._HAP_HASCHILDREN) == 0:  # node is a leaf
            return True
        else:
            return False

    def _traverse_branch(self, node: win32.CDispatch) -> dict:
        """Traverse the branch through recursion and return its nodes as JSON tree
        dictionary.

        Parameters
        ----------
        node : win32.CDispatch
            Node to be traversed.

        Returns
        -------
        dict
            Dictionary compatible with JSON structure. The keys are:
                'node' - name of the node;
                'children' - if this key is present, then its value returns the
                    list of children pertaining to the `node`;
        """
        n = {'node': node.Name}
        if not self._isleaf(node):
            n['children'] = [self._traverse_branch(child)
                             for child in node.Elements]
        else:
            # node is a leaf, if the value is a float and not None append its
            # units
            if node.ValueType == 2 and node.Value is not None:
                n['value'] = node.Value
                n['units'] = node.UnitString

        return n

    def _get_simulation_node_names(self) -> dict:
        """Get the names of the stream and blocks in simulation.

        Returns
        -------
        dict
            JSON compatible dictionary containing the nodes names of streams
            and blocks in simulation.
        """
        sim_nodes = {'Streams': {}, 'Blocks': {},
                     'Flowsheeting Options\\Design-Spec': {}}
        for node in sim_nodes:
            for o in self._aspen.Tree.FindNode("\\Data\\" + node).Elements:
                sim_nodes[node][o.Name] = o.AttributeValue(
                    self._HAP_RECORDTYPE)

        return sim_nodes

    def _build_nodes(self, simulation_node: dict, root_node: dict,
                     nodetype: str, iotype: str) -> None:
        """Build the nodes of the simulation (both streams and blocks).

        Parameters
        ----------
        simulation_node : dict
            Dictionary contaning the names of the blocks/streams as keys and
            the values as blocks/streams types.
        root_node : dict
            Dictionary containing the root node where its branches will be
            appended.
        nodetype : str
            Type of node of `simulation_node` and `root_node`. Valid values are
            'blocks' and 'streams'.
        iotype : str
            Type of input/output data from node to be built. Valid values are
            'input' and 'output'

        Notes
        -----
        This function does not return values. It only works on the references
        of `root_node`. Thus this variable will be altered.
        """
        iotypes = ['input', 'output']
        nodetypes = ['blocks', 'streams', 'des_spec']
        if iotype not in iotypes:
            raise ValueError(
                "Invalid IO type specification. "
                "Valid values are 'input' and 'output'."
            )

        if nodetype not in nodetypes:
            raise ValueError(
                "Invalid node type specification. "
                "Valid values are 'blocks', 'streams' and 'des_spec'."
            )

        # if the node name is present in the catalogue, build the branches for
        # that node
        if nodetype == 'blocks':
            INPUT_CATALOGUE = BLOCKS_CATALOGUE['Input']
            OUTPUT_CATALOGUE = BLOCKS_CATALOGUE['Output']

            nodetype = nodetype.capitalize()

        elif nodetype == 'streams':
            INPUT_CATALOGUE = STREAMS_CATALOGUE['Input']
            OUTPUT_CATALOGUE = STREAMS_CATALOGUE['Output']

            nodetype = nodetype.capitalize()

        else:
            INPUT_CATALOGUE = DESPEC_CATALOGUE['Input']
            OUTPUT_CATALOGUE = DESPEC_CATALOGUE['Output']

            # swap to an aspen accepted node name since that the design spec
            # node is inside flowsheeting options
            nodetype = 'Flowsheeting Options\\Design-Spec'

        # grab the catalogue for that block
        if iotype == 'input':
            CATALOGUE = INPUT_CATALOGUE
        else:
            CATALOGUE = OUTPUT_CATALOGUE

        for node in simulation_node:

            if simulation_node[node] in INPUT_CATALOGUE and \
                    simulation_node[node] in OUTPUT_CATALOGUE:

                var_catalogue = copy.deepcopy(CATALOGUE[simulation_node[node]])
                leaves = sorted(var_catalogue, key=lambda k: k['Name'])

                for leaf in leaves:
                    # rename the 'Name' key to 'node'
                    leaf['node'] = leaf.pop('Name')

                    if 'Description' in leaf:
                        leaf['description'] = leaf.pop('Description')

                    # append children nodes if they exist
                    node_path = self._NODE_PATH_FORMAT.format(
                        nodetype,
                        node,
                        iotype.capitalize(),
                        leaf['node']
                    )
                    children_node_ph = self._aspen.Tree.FindNode(node_path)

                    if children_node_ph is None:
                        # node not found, raise exception
                        raise ValueError(
                            "Can't find path: \n{0}".format(node_path)
                        )
                    children_nodes = self._traverse_branch(children_node_ph)
                    if any(x in children_nodes for x in ['children', 'value']):
                        leaf.update(children_nodes)

                leaves_node = {'node': iotype.capitalize(), 'children': leaves}

                node_to_append = {'node': node, 'children': [leaves_node]}

                # check the node already exists. If so, update its entries
                node_check = [child['node'] ==
                              node for child in root_node['children']]
                if any(node_check):
                    root_node['children'][node_check.index(
                        True)]['children'].append(leaves_node)
                else:
                    if 'children' in root_node:
                        # there exists children, just append new nodes
                        root_node['children'].append(node_to_append)
                    else:
                        # the root_node wasn't initialized with children list
                        root_node['children'] = [node_to_append]

            else:
                if simulation_node[node] not in INPUT_CATALOGUE or \
                        simulation_node[node] not in OUTPUT_CATALOGUE:
                    raise KeyError(
                        "{0} type {1} not inplemented in {0} {1} catalogue."
                        .format(nodetype.capitalize(), iotype))

    def _prune_leaves(self, root_node) -> dict:
        """Prune all the leaves that does not have 'value' attribute in them.
        In other words, remove the leaves that user did not set in file.

        Parameters
        ----------
        root_node : dict
            Branch to be pruned.

        Returns
        -------
        dict
            Pruned branch.
        """
        importer = DictImporter()
        exporter = DictExporter()

        inptree = importer.import_(root_node)

        # keep checking for leaves without value attribute
        while True:
            all_has_value = all(hasattr(leaf, 'value')
                                for leaf in inptree.leaves)

            if all_has_value:
                break

            for leaf in inptree.leaves:
                if not hasattr(leaf, 'value'):
                    # prune leaves without value attribute
                    leaf.parent = None

        return exporter.export(inptree)

    # --------------------------- PUBLIC FUNCTIONS --------------------------
    def open_connection(self) -> None:
        """Opens the COM/OLE server of an Aspen Plus application.
        """
        self._aspen = win32.Dispatch('Apwn.Document')
        self._aspen.InitFromArchive2(pathlib.Path(self._aspen_filepath))

    def close_connection(self) -> None:
        """Closes the COM/OLE server and connection of an Aspen Plus application.
        """
        if self._aspen is not None:
            self._aspen.Quit()
            self._aspen = None

    def get_simulation_data(self) -> dict:
        """Returns the simulation data dictionary with blocks names, components,
        streams, etc.

        Returns
        -------
        dict
            Dictionary containing the following keys -- values pairs:
            'components'    --  Components in simulation (list);
            'therm_method'  --  Thermodynamic model set in simulation (list);
            'blocks'        --  Blocks in simulation (list);
            'streams'       --  Streams in simulation (list);
            'reactions'     --  Reactions in simulation (list);
            'sens_analysis' --  Sensitivity analysis in simulation (list);
            'calculators'   --  Calculators in simulation (list);
            'optimizations' --  Optimizations in simulation (list);
            'design_specs'  --  Design Specifications in simulation (list);
        """

        node_paths = {
            'components': r"\Data\Components\Specifications\Input\TYPE",
            'therm_method': r"\Data\Properties\Specifications\Input\GOPSETNAME",
            'blocks': r"\Data\Blocks",
            'streams': r"\Data\Streams",
            'reactions': r"\Data\Reactions\Reactions",
            'sens_analysis': r"\Data\Model Analysis Tools\Sensitivity",
            'calculators': r"\Data\Flowsheeting Options\Calculator",
            'optimizations': r"\Data\Model Analysis Tools\Optimization",
            'design_specs': r"\Data\Flowsheeting Options\Design-Spec"}

        simulation_data = {'components': [''],
                           'therm_method': [''],
                           'blocks': [''],
                           'streams': [''],
                           'reactions': [''],
                           'sens_analysis': [''],
                           'calculators': [''],
                           'optimizations': [''],
                           'design_specs': ['']}

        if self._aspen is None:
            self.open_connection()

        try:
            for k in node_paths:
                node = self._aspen.Tree.FindNode(node_paths[k])
                if k == 'therm_method':
                    simulation_data[k] = [node.Value]
                else:
                    simulation_data[k] = [o.Name for o in node.Elements]
        except AttributeError:
            raise AttributeError("Couldn't retrieve simulation data "
                                 "due pre specified nodes not being "
                                 "accessible.")

        return simulation_data

    def get_connection_object(self) -> win32.CDispatch:
        """Returns the aspen object connection reference.

        Returns
        -------
        win32.CDispatch
            COM Object Apwn.Document.
        """
        if self._aspen is None:
            self.open_connection()

        return self._aspen

    def get_simulation_partial_io_tree(self, iotype: str) -> dict:
        """Builds partial (input or output) blocks and streams branches in a
        single tree.

        Parameters
        ----------
        iotype : str
            Type of input/output data from node to be built. Valid values are
            'input' and 'output'.

        Returns
        -------
        dict
            JSON compatible tree.
        """
        if iotype != 'input' and iotype != 'output':
            raise ValueError(
                "Invalid IO type specification. "
                "Valid values are 'input' and 'output'."
            )
        else:
            if iotype == 'output':
                # when sampling results, ensure that all nodes are built
                self._check_simulation_results()

        # open the connection if it is not opened
        if self._aspen is None:
            self.open_connection()

        # build root nodes
        sim_nodes = self._get_simulation_node_names()

        root_block = {'node': 'Blocks', 'children': []}
        root_stream = {'node': 'Streams', 'children': []}
        root_desspec = {'node': 'Design-Spec', 'children': []}
        root_node = {
            'node': 'Data',
            'children':
            [
                root_block,
                root_stream,
                {'node': 'Flowsheeting Options', 'children': [root_desspec]}
            ]}

        # streams
        self._build_nodes(sim_nodes['Streams'], root_stream,
                          'streams', iotype)

        # blocks
        self._build_nodes(sim_nodes['Blocks'], root_block,
                          'blocks', iotype)

        # design specs
        self._build_nodes(sim_nodes['Flowsheeting Options\\Design-Spec'],
                          root_desspec, 'des_spec', iotype)

        if iotype == 'input':
            root_node = self._prune_leaves(root_node)

        return root_node

    def get_simulation_tree(self) -> dict:
        """Builds full blocks and streams branches in a single tree.

        Returns
        -------
        dict
            JSON compatible tree.
        """
        # open the connection if it is not opened
        if self._aspen is None:
            self.open_connection()

        # check if the simulation has results
        self._check_simulation_results()

        # build root nodes
        sim_nodes = self._get_simulation_node_names()

        root_block = {'node': 'Blocks', 'children': []}
        root_stream = {'node': 'Streams', 'children': []}
        root_node = {'node': 'Data', 'children': [root_block, root_stream]}

        # streams
        self._build_nodes(sim_nodes['Streams'], root_stream,
                          'streams', 'input')
        self._build_nodes(sim_nodes['Streams'], root_stream,
                          'streams', 'output')

        # blocks
        self._build_nodes(sim_nodes['Blocks'], root_block,
                          'blocks', 'input')
        self._build_nodes(sim_nodes['Blocks'], root_block,
                          'blocks', 'output')

        return root_node


if __name__ == "__main__":
    from tests_.mock_data import ASPEN_BKP_FILE_PATH
    # filepath = r"C:\Users\Felipe\Desktop\GUI\python\infill.bkp"
    filepath = ASPEN_BKP_FILE_PATH
    con_obj = AspenConnection(filepath)

    print(con_obj.get_simulation_data())

    import json
    # print(json.dumps(con_obj.get_simulation_partial_io_tree('input'), indent=2))
    # print(json.dumps(con_obj.get_simulation_partial_io_tree('output'), indent=2))
    print(json.dumps(con_obj.get_simulation_tree(), indent=4))

    del con_obj
