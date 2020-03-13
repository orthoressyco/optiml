import matplotlib.pyplot as plt
import numpy as np

from optimization.constrained.projected_gradient import ConstrainedOptimizer


class ActiveSet(ConstrainedOptimizer):
    # Apply the Active Set Method to the convex Box-Constrained Quadratic
    # program
    #
    #  (P) min { (1/2) x^T * Q * x + q * x : 0 <= x <= u }
    #
    # Input:
    #
    # - BCQP, the structure encoding the BCQP to be solved within its fields:
    #
    #   = BCQP.Q: n \times n symmetric positive semidefinite real matrix
    #
    #   = BCQP.q: n \times 1 real vector
    #
    #   = BCQP.u: n \times 1 real vector > 0
    #
    # - MaxIter (integer scalar, optional, default value 1000): the maximum
    #   number of iterations
    #
    # Output:
    #
    # - v (real scalar): the best function value found so far (possibly the
    #   optimal one)
    #
    # - x ([ n x 1 ] real column vector, optional): the best solution found so
    #   far (possibly the optimal one)
    #
    # - status (string, optional): a string describing the status of the
    #   algorithm at termination, with the following possible values:
    #
    #   = 'optimal': the algorithm terminated having proven that x is a(n
    #     approximately) optimal solution, i.e., the norm of the gradient at x
    #     is less than the required threshold
    #
    #   = 'stopped': the algorithm terminated having exhausted the maximum
    #     number of iterations: x is the bast solution found so far, but not
    #     necessarily the optimal one

    def __init__(self, f, eps=1e-6, max_iter=1000, verbose=False, plot=False):
        super().__init__(f, eps, max_iter, verbose, plot)

    def minimize(self, ub):

        self.wrt = ub / 2  # start from the middle of the box
        v = self.f.function(self.wrt)

        # Because all constraints are box ones, the active set is logically
        # partitioned onto the set of lower and upper bound constraints that are
        # active, L and U respectively. Of course, L and U have to be disjoint.
        # Since we start from the middle of the box, both the initial active sets
        # are empty
        L = false(n, 1)
        U = false(n, 1)

        # the set of "active variables", those that do *not* belong to any of the
        # two active sets and therefore are "free", is therefore the complement to
        # 1 : n of L union U; since L and U are empty now, A = 1 : n
        A = true(n, 1)

        print('iter\tf(self.wrt)\t\t| B |\tI/O')

        while True:

            print('%4d\t%1.8e\t%d\t'), i, v, sum(L) + sum(U)

            if i > self.max_iter:
                status = 'stopped'
                break

            # solve the *unconstrained* problem restricted to A the problem reads:
            #
            #  min { (1/2) x_A' * Q_{AA} * x_A + ( q_A + u_U' * Q_{UA} ) * x_A }
            #    [ + (1/2) x_U' * Q_{UU} * x_U ]
            #
            # and therefore the optimal solution is:
            #
            #   x_A^* = - Q_{AA}^{-1} ( q_A + u_U' * Q_{UA} )
            #
            # not that this actually is a *constrained* problem subject to equality
            # constraints, but in our case equality constraints just fix variables
            # (and anyway, any QP problem with equality constraints reduces to an
            # unconstrained one)

            xs = np.zeros(n, 1)
            xs[U].lvalue = ub[U]
            opts.SYM = true  # tell it Q_{AA} is positive definite (hence of
            opts.POSDEF = true  # course symmetric), it'll probably do the right
            # thing and use Cholesky to solve the system
            xs[A].lvalue = linsolve(BCQP.Q(A, A), -(BCQP.q(A) + BCQP.Q(A, U) * ub[U]), opts)

            if np.all(xs[A] <= np.logical_and(ub[A] + 1e-12, xs[A] >= -1e-12)):
                # the solution of the unconstrained problem is actually feasible

                # move the current point right there
                self.wrt = xs

                # compute function value and gradient
                v, g = self.f.function(self.wrt), self.f.jacobian(self.wrt)

                h = find(np.logical_and(L, g < -1e-12))
                if h:
                    uppr = False
                else:
                    h = find(np.logical_and(U, g > 1e-12))
                    uppr = True

                if not h:
                    print('\nOPT\t%1.8e\n'), v)
                    status = 'optimal'
                    break
                else:
                    h = h(1, 1)  # that's probably Bland's anti-cycle rule
                    A(h).lvalue = True
                    if uppr:
                        U(h).lvalue = False
                        print('O %d(U)'.format(h))
                    else:
                        L(h).lvalue = False
                        print('O %d(L)\n'.format(h))
            else:  # the solution of the unconstrained problem is *not* feasible
                # this means that d = xs - self.wrt is a descent direction, use it
                # of course, only the "free" part really needs to be computed

                d = np.zeros(n, 1)
                d[A].lvalue = xs[A] - self.wrt(A)

                # first, compute the maximum feasible step size max_t such that:
                #   0 <= self.wrt[i] + max_t * d[i] <= u[i]   for all i

                idx = np.logical_and(A, d > 0)  # positive gradient entries
                max_t = min((ub[idx] - self.wrt(idx)) / d[idx])
                idx = np.logical_and(A, d < 0)  # negative gradient entries
                max_t = min(max_t, min(-self.wrt(idx) / d[idx]))

                # it is useless to compute the optimal t, because we know already
                # that it is 1, whereas max_t necessarily is < 1
                self.wrt = self.wrt + max_t * d

                # compute function value
                v = self.f.function(self.wrt)

                # update the active set(s)
                nL = np.logical_and(A, self.wrt <= 1e-12)
                L(nL).lvalue = True
                A(nL).lvalue = False

                nU = np.logical_and(A, self.wrt >= ub - 1e-12)
                U(nU).lvalue = True
                A(nU).lvalue = False

                print('I %d+%d\n'.format(sum(nL), sum(nU)))

            self.iter += 1

        if self.verbose:
            print()
        if self.plot and self.n == 2:
            plt.show()
        return self.wrt, status
