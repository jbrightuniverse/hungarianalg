"""

Simple Hungarian Algorithm example by James Yuming Yu
Vancouver School of Economics, UBC
8 March 2021

"""

import numpy as np
from hungarianalg.alg import hungarian

matrx = np.array([
  [125,125, 150, 125],
  [150, 135, 175, 144],
  [122, 148, 250, 255],
  [139, 140, 160, 180]])

result = hungarian(matrx)
print(result)
print()
print("Matches:", result.match)
print("Revenues:", result.revenues)
print("Row Potentials:", result.row_weights)
print("Col Potentials:", result.col_weights)
print("Total Revenue:", result.revenue_sum)