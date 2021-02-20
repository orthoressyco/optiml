import numpy as np

from . import StochasticOptimizer


class RMSProp(StochasticOptimizer):

    def __init__(self,
                 f,
                 x=None,
                 batch_size=None,
                 eps=1e-6,
                 epochs=1000,
                 step_size=0.001,
                 decay=0.9,
                 callback=None,
                 callback_args=(),
                 shuffle=True,
                 random_state=None,
                 verbose=False):
        super().__init__(f=f,
                         x=x,
                         step_size=step_size,
                         batch_size=batch_size,
                         eps=eps,
                         epochs=epochs,
                         callback=callback,
                         callback_args=callback_args,
                         shuffle=shuffle,
                         random_state=random_state,
                         verbose=verbose)
        if not 0 <= decay < 1:
            raise ValueError('decay has to lie in [0, 1)')
        self.decay = decay
        self.moving_mean_squared = np.ones_like(self.x)

    def minimize(self):

        self._print_header()

        for batch in self.batches:

            self.f_x = self.f.function(self.x, *batch)

            self._print_info()

            try:
                self.callback(batch)
            except StopIteration:
                break

            if self.is_batch_end():
                self.epoch += 1

            if self.epoch >= self.epochs:
                self.status = 'stopped'
                break

            self.g_x = self.f.jacobian(self.x, *batch)

            # compute search direction
            d = -self.g_x

            self.moving_mean_squared = self.decay * self.moving_mean_squared + (1. - self.decay) * self.g_x ** 2

            if self.is_lagrangian_dual():
                # project the direction over the active constraints
                d[np.logical_and(self.x <= 1e-12, d < 0)] = 0

                # first, compute the maximum feasible step size max_t such that:
                #
                #   0 <= lambda[i] + max_t * d[i] / sqrt(moving_mean_squared)   for all i

                idx = d < 0  # negative gradient entries
                if any(idx):
                    max_t = min(-self.x[idx] / d[idx] * np.sqrt(self.moving_mean_squared[idx]))
                    self.step_size = max_t

            step = self.step_size * d / np.sqrt(self.moving_mean_squared)

            self.x += step

            self.iter += 1

        if self.verbose:
            print('\n')

        if self.is_lagrangian_dual():
            assert all(self.x >= 0)  # Lagrange multipliers

        return self
