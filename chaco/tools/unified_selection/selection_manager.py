#------------------------------------------------------------------------------
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import numpy as np

from traits.api import HasTraits, Dict, Event


class SelectionManager(HasTraits):
    """ A manager to aggregate and collapse selections.

    """
    _selections = Dict
    selection_changed = Event

    def set_selection(self, source_id, selection):
        """ Set a selection in the manager or add it if it doesn't exist.

        Parameters:
        -----------
        source_id : str
            A unique id for the selection source.

        selection : numpy.ndarray
            A numpy array to use as a selection mask. Should only contain
            boolean values.

        """
        if not all(isinstance(x, (int, float)) for x in selection.tolist()):
            raise ValueError('All values in a selection must have an explicit'
                             ' truth value. Got %s instead.' % selection)

        self._selections[source_id] = selection

    def get_selection(self, source_id):
        """ Get the selection for a given id.

        Parameters:
        -----------
        source_id : str
            The id for the requested source.

        Returns:
        --------
        A numpy array representing the selection for the given id or None.

        """
        return self._selections.get(source_id)

    def remove_selection(self, source_id):
        """ Remove the selection for a given id.

        Parameters:
        -----------
        source_id : str
            The id of the selection to remove.

        """
        if source_id in self._selections:
            del self._selections[source_id]

    def collapse_selections(self):
        """ Collapse all of the selections into one final selection.

        Returns:
        --------
        A selection mask that represents the logical AND of all the
        selections.

        """
        return np.logical_and.reduce(self._selections.values())

    def __selections_items_changed(self, new):
        """ Fires the `selections_changed` event when the `_selections`
        dictionary changes.

        """
        self.selection_changed = self.collapse_selections()
