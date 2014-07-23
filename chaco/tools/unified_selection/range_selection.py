#------------------------------------------------------------------------------
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import numpy as np

from traits.api import Property, Either, Array

from chaco.tools.range_selection import RangeSelection as _RangeSelection
from base_unified_selection_tool import BaseUnifiedSelectionTool


class RangeSelection(BaseUnifiedSelectionTool, _RangeSelection):
    """ A subclass of RangeSelection that implements the IUnifiedSelectionTool
    interface.

    """
    #: A redefined selection mask that allows a value of None.
    _selection_mask = Property(Either(Array, None))

    def __selection_mask_default(self):
        """ The default selection mask is a numpy array of all False in the
        shape of the data.

        """
        data_source = self.get_data_source()
        if data_source:
            return np.zeros_like(data_source.get_data(), dtype=bool)
        return None

    def _get_selection(self):
        """ Reimplemented property getter for `selection`.

        """
        data_source = self.get_data_source()
        if data_source:
            return data_source.metadata.get(self.metadata_name)
        return None

    def _set_selection(self, val):
        """ Reimplemented property setter for `selection`.

        """
        data_source = self.get_data_source()
        manager = self.get_manager()
        old = None

        if data_source and manager:
            md = data_source.metadata
            old = md.get(self.metadata_name)

            if val is not None:
                md[self.metadata_name] = val

                data = data_source.get_data()
                new_mask = np.zeros_like(data, dtype=bool)
                low, high = val

                pts = (data >= low) & (data <= high)
                if self.selection_mode == 'exclude':
                    new_mask &= ~pts
                elif self.selection_mode == 'invert':
                    new_mask[pts] ^= True
                else:
                    new_mask |= pts

                orig_mask = self._selection_mask
                should_set_mask = (
                    orig_mask is None
                    or not np.array_equal(new_mask, orig_mask)
                )

                if should_set_mask:
                    self._selection_mask = new_mask

            else:
                self._selection_mask = None
                manager.remove_selection(id(self))

        self.trait_property_changed('selection', old, val)

        for l in self.listeners:
            if hasattr(l, "set_value_selection"):
                l.set_value_selection(val)

    def _get__selection_mask(self):
        """ Reimplemented property getter for `_selection_mask`.

        """
        manager = self.get_manager()
        if manager:
            return manager.get_selection(id(self))

    def _set__selection_mask(self, mask):
        """ Reimplemented property setter for `_selection_mask`.

        """
        manager = self.get_manager()
        if manager:
            if mask is not None:
                manager.set_selection(id(self), mask)
            else:
                manager.remove_selection(id(self))

    def tuple_from_mask(self, mask):
        """ Convert a numpy mask to a tuple selection.

        Parameters:
        -----------
        mask : numpy.ndarray
            The mask to convert.

        Returns:
        --------
        A tuple of format (low, high).

        """
        data_source = getattr(self.plot, self.axis, None)

        if data_source:
            data = data_source.get_data()
            region = np.where(mask == 1)[0]

            if not region.any():
                return None

            low = data[(min(region))]
            high = data[(max(region))]
            return (low, high)

        return None

    def update_selection_from_mask(self, mask):
        """ Implemented for BaseUnifiedSelectionTool. Sets the RangeSelection's
        selection from a given mask.

        """
        self.selection = self.tuple_from_mask(mask)
