# Implement Newton's method for finding roots (zeroes) of
# differentiable, real-valued functions. The function ‹newton› takes
# 4 arguments: the function ‹f› for which we are finding the root,
# its first derivative ‹df›, the initial guess ‹ini› and the
# precision ⟦p⟧ = ‹prec›. Return a number ⟦x⟧, such that ⟦∃u ∈ ⟨x -
# p, x + p⟩. f(u) = 0⟧.

# How it works: if you have an estimate ⟦x₀⟧ for ⟦x⟧, you can get a
# better estimate by subtracting ⟦f(x₀)/f'(x₀)⟧ from ⟦x₀⟧ (where
# ⟦f'⟧ is the derivative, ‹df›). Repeat until satisfied (you can
# assume quadratic convergence, meaning that the error is bounded by
# the improvement one step earlier).

def newton( f, df, ini, prec ): pass

# Using ‹newton›, implement a cube root function. Hint: given ⟦z⟧
# (the number to be cube-rooted), find a function ⟦f(x)⟧ such that
# ⟦f(x) = 0⟧ iff ⟦z = x³⟧. Clearly, the zero of ⟦f⟧ is the cube root
# of ⟦z⟧. The meaning of ‹prec› is the same as in ‹newton›.

def cbrt( z, prec ): pass

# Note: if all inputs are integers, make sure the functions use
# integers throughout, so that they can be used with very large
# numbers. In type annotations, using ‹float› is OK, because mypy
# treats float as a superclass of ‹int› (which is very wrong, but
# alternatives are… complicated).

def test_float() -> None:
    from math import sin, cos, pi
    assert abs( cbrt(  8, 0.0001 ) - 2 ) < 0.0001, cbrt( 8, 0.0001 )
    assert abs( cbrt( 27, 0.0001 ) - 3 ) < 0.0001
    assert 1.2599210498 <= cbrt(  2, 1e-10 ) <= 1.25992105, cbrt( 2, 1e-10 )
    pi_ = 2 * newton( cos, lambda x: -sin( x ), 1, 0.0001 )
    assert abs( pi_ - pi ) < 0.0002, pi_


def test_int() -> None:
    assert 10**101 - 10 <= cbrt( 10**303, 10 ) <= 10**101 + 10
    x0 = 10**303 + 10**225
    cbrt_x0 = 10**101 + 33333333333333333333333
    assert cbrt_x0 ** 3 <= x0 <= ( cbrt_x0 + 1 ) ** 3
    assert cbrt_x0 - 10 <= cbrt( x0, 10 ) <= cbrt_x0 + 10


if __name__ == '__main__':
    test_float()
    test_int()
