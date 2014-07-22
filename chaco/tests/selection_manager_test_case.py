#------------------------------------------------------------------------------
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest

import numpy as np

from chaco.tools.unified_selection.api import SelectionManager


class SelectionManagerTestCase(unittest.TestCase):
    """ A class to test the functionality of the SelectionManager.

    """
    def setUp(self):
        """ Create the selection manager.

        """
        self.manager = SelectionManager()

    def test_add_selection(self):
        """ Test the addition of selections to the manager.

        """
        select = np.array([True, False, True, False])
        _id = 'selectionone'
        self.manager.add_selection(_id, select)

        self.assertEqual(self.manager._selections, {_id: select})

    def test_add_invalid_selection(self):
        """ Test that adding a selection with non-boolean values raises
        an error.

        """
        invalid = np.array(['string', True, False])
        self.assertRaises(ValueError, self.manager.add_selection,
                          'invalid', invalid)

    def test_get_selection(self):
        """ Test the fetching of selections from the manager.

        """
        select = np.array([True, False, True, False])
        _id = 'selectionone'
        self.manager.add_selection(_id, select)

        self.assert_(np.array_equal(self.manager.get_selection(_id), select))

    def test_remove_selection(self):
        """ Test the removal of selections from the manager.

        """
        select_one = np.array([True, False, True, False])
        select_two = np.array([False, False, True, True])

        self.manager.add_selection('selectone', select_one)
        self.manager.add_selection('selecttwo', select_two)

        self.manager.remove_selection('invalid_id')
        self.assertEqual(self.manager._selections, {'selectone': select_one,
                                                    'selecttwo': select_two})

        self.manager.remove_selection('selecttwo')
        self.assertEqual(self.manager._selections, {'selectone': select_one})

    def test_collapse_selection(self):
        """ Test the collapsing of selections.

        """
        select_one = np.array([True, False, True, False])
        select_two = np.array([False, False, True, True])

        self.manager.add_selection('selectionone', select_one)
        self.manager.add_selection('selectiontwo', select_two)

        self.assert_(np.array_equal(self.manager.collapse_selections(),
                                    np.array([False, False, True, False])))

    def test_selection_changed(self):
        """ Test the `selection_changed` event.

        """
        expected = np.array([False, True, True, False])

        def _handler(val):
            self.assert_(np.array_equal(val, expected))

        one = np.array([True, True, True, False])
        self.manager.add_selection('one', one)

        self.manager.on_trait_event(_handler, 'selection_changed')

        two = np.array([False, True, True, False])
        self.manager.add_selection('two', two)


if __name__ == "__main__":
    unittest.main()
