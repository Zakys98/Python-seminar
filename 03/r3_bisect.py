from typing import Callable

# Write a function ‹bisect›, which takes ⟦f⟧ which is a continuous
# function, two numbers, ⟦x₁⟧ and ⟦x₂⟧ such that ⟦\sgn(f(x₁)) ≠
# \sgn(f(x₂))⟧ and precision ⟦p⟧. Return ⟦x⟧ such that ⟦∃z. x - p ≤
# z ≤ x + p ∧ f(z) = 0⟧.

def bisect( f, x_1, x_2, prec ): pass


def test_main() -> None:
    prec = 0.0001

    def check( result: float, expected: float ) -> None:
        assert abs( result - expected ) <= prec

    check( bisect( lambda x: x, 10, -6, prec ), 0 )
    check( bisect( lambda x: x, -6, 10, prec ), 0 )
    check( bisect( lambda x: x, -10, 6, prec ), 0 )
    check( bisect( lambda x: x - 2, 0, 3, prec ), 2 )
    check( bisect( lambda x: x ** 2 - 9, 0, 5, prec ), 3 )
    check( bisect( lambda x: x ** 2 - 9, -5, 0, prec ), -3 )
    check( bisect( lambda x: x ** 5 - x ** 3 + 2, -7, 3,
                   prec ), -1.34787 )

if __name__ == "__main__":
    test_main()
