#------------------------------------------------------------------------------
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import HasTraits


class BaseUnifiedSelectionTool(HasTraits):
    """ A base class for all tools that support unified selection.

    """
    def register(self, manager):
        """ Register this tool with a manager. The manager does not store any
        reference to the tool itself, only hooks up the appropriate events and
        sets itself as the selection manager for the tool's data source.

        Parameters:
        -----------
        tool : Chaco tool
            The tool to register.

        """
        data_source = getattr(self.plot, self.axis, None)
        if data_source:
            data_source.selection_manager = manager
            manager.on_trait_event(self.update_selection_from_mask,
                                   'selection_changed')

    def get_manager(self):
        """ Get the manager for this tool.

        Returns:
        --------
        The manager for this tool's data source or None.
        """
        data_source = self.get_data_source()
        if data_source:
            return getattr(data_source, 'selection_manager', None)

    def get_data_source(self):
        """ Get the data source for this tool.

        Returns:
        --------
        The data source for this tool or None.

        """
        return getattr(self.plot, self.axis, None)

    def update_selection_from_mask(self, mask):
        """ Updates the tool's selection via a selection mask. This method
        must be implemented by subclasses.

        Parameters:
        -----------
        mask : np.ndarray
            The mask to derive the selection from.

        """
        raise NotImplementedError
