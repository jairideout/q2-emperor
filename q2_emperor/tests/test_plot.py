# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

import pandas as pd
import numpy as np
import qiime2
import skbio

from q2_emperor import plot


class PlotTests(unittest.TestCase):
    def setUp(self):
        eigvals = np.array([0.50, 0.25, 0.25])
        samples = np.array([[0.1, 0.2, 0.3],
                            [0.2, 0.3, 0.4],
                            [0.3, 0.4, 0.5],
                            [0.4, 0.5, 0.6]])
        proportion_explained = pd.Series([15.5, 12.2, 8.8],
                                         index=['PC1', 'PC2', 'PC3'])
        samples_df = pd.DataFrame(samples,
                                  ['A', 'B', 'C', 'D'],
                                  ['PC1', 'PC2', 'PC3'])
        self.pcoa = skbio.OrdinationResults(
                'PCoA',
                'Principal Coordinate Analysis',
                eigvals,
                samples_df,
                proportion_explained=proportion_explained)
        self.metadata = qiime2.Metadata(
            pd.DataFrame({'val1': ['1.0', '2.0', '3.0', '4.0']},
                         index=['A', 'B', 'C', 'D']))

    def test_plot(self):
        with tempfile.TemporaryDirectory() as output_dir:
            plot(output_dir, self.pcoa, self.metadata)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue('src="./emperor.html"' in open(index_fp).read())

    def test_plot_custom_axes(self):
        with tempfile.TemporaryDirectory() as output_dir:
            plot(output_dir, self.pcoa, self.metadata, custom_axis='val1')
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue('src="./emperor.html"' in open(index_fp).read())
