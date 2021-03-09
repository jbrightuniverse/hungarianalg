A Python 3 implementation of the Hungarian Algorithm for optimal matching in bipartite weighted graphs.

Based on the graph theory implementation in [these notes](http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf) combined with the matrix interpretation in [these notes](https://montoya.econ.ubc.ca/Econ514/hungarian.pdf).

For a detailed overview, see [this Jupyter notebook](https://github.com/jbrightuniverse/Hungarian-Algorithm-No.-5/blob/main/HungarianAlgorithm.ipynb).

# Usage

Installation: `pip3 install hungarianalg`

Import: `from hungarianalg.alg import hungarian`

Function call: `result = hungarian(matrix)`

Properties:
- Optimal Matching: `result.match`
- Revenues: `result.revenues`
- Row Weights: `result.row_weights`
- Col Weights: `result.col_weights`
- Total Revenue: `result.revenue_sum`

See `example.py` for a comprehensive example.
