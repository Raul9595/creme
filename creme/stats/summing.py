from .. import utils

from . import base


class Sum(base.Univariate):
    """Running sum.

    Attributes:
        sum (float) : The running sum.

    Example:

        ::

            >>> from creme import stats

            >>> X = [-5, -3, -1, 1, 3, 5]
            >>> mean = stats.Sum()
            >>> for x in X:
            ...     print(mean.update(x).get())
            -5.0
            -8.0
            -9.0
            -8.0
            -5.0
            0.0

    """

    def __init__(self):
        self.sum = 0.

    @property
    def name(self):
        return 'sum'

    def update(self, x):
        self.sum += x
        return self

    def get(self):
        return self.sum


class RollingSum(base.Univariate, utils.Window):
    """Running sum over a window.

    Parameters:
        window_size (int): Size of the rolling window.

    Attributes:
        sum (int): The running rolling sum.

    Example:

        ::

            >>> from creme import stats

            >>> X = [1, -4, 3, -2, 2, 1]
            >>> rolling_sum = stats.RollingSum(2)
            >>> for x in X:
            ...     print(rolling_sum.update(x).get())
            1
            -3
            -1
            1
            0
            3

    """

    def __init__(self, window_size):
        super().__init__(size=window_size)
        self.sum = 0

    @property
    def window_size(self):
        return self.size

    @property
    def name(self):
        return f'rolling_{self.size}_sum'

    def update(self, x):
        if len(self) == self.size:
            self.sum -= self[0]
        self.sum += x
        self.append(x)
        return self

    def get(self):
        return self.sum
