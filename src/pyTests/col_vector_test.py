from __future__ import print_function

import numpy as np
import pygamma

if __name__ == "__main__":

    cc = (pygamma.col_vector.from_array([1,2,3]),)

         

#    cc = (pygamma.col_vector(),
#          pygamma.col_vector(3),
#          pygamma.col_vector(3,1),
#          pygamma.col_vector([1,2,3]),
#          pygamma.col_vector(np.array([1,2,3]))
#         )

#    for cv in cc:
#        print("cv[:] = ", cv[:])

    for cv in cc:
        print("cv = ", cv)

    for cv in cc:
        print("cv.__repr__() = ", cv.__repr__())

