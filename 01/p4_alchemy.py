# You are given:
#
#  • a list of «available» substances and their quantities,
#  • a list of «desired» substances and their quantities,
#  • a list of «transmutation rules», where each is a 2-tuple:
#    ◦ first element is the list of required inputs,
#    ◦ the second element is the list of outputs,
#    ◦ both input and output is a tuple of an element and quantity.
#
# The sum of the quantities on the right hand side of the list is
# strictly less than that on the left side. Decide whether it is
# possible to get from the available substances to the desired,
# using the given rules: return a boolean. It does not matter
# whether there are leftovers. Rules can be used repeatedly.

def alchemy(available, desired, rules):
    if len(rules) == 0:
        return True
    for des, number in desired:
        print(des)
        founded_rules = []
        for input, out in rules:
            if des == out[0][0]:
                founded_rules.append(input)
        print(founded_rules)
        for found_rule in founded_rules:
            for ingr in found_rule:
                for avl in available:
                    if ingr[0] == avl[0]:
                        if avl[1] < ingr[1]:
                            return False
                        
        #rules_des = [des == out for _, out in rules]
    return False

# The rules from tests in a more readable format, for your convenience:
#
#  • 3 chamomile, 4 water, 1 verbena, 2 valerian → relaxing concoction
#  • 7 ethanol → elixir of life
#  • 4 water, 2 mandrake, 2 valerian, nightshade → elixir of life
#  • 5 tea leaves → tea tree oil
#  • 2 primrose oil, 2 water, 1 tea tree oil → skin cleaning oil
#  • 1 iron, 1 carbon → steel
#  • 1 footprint → 1 carbon
#  • 6 ice → 5 water
#  • 3 steel → 1 cable
#  • 10 lead, philosopher stone, 2 unicorn hair → 10 gold

def test_main():
    rules = [ ( [ ( 'tea leaves', 5 ) ], [ ( 'tea tree oil', 1 ) ] ),

              ( [ ( 'primrose oil', 2 ), ( 'water', 2 ),
                  ( 'tea tree oil', 1 ) ],
                [ ( 'skin cleaning oil', 1 ) ] ),

              ( [ ( 'footprint', 1 ) ], [ ( 'carbon', 1 ) ] ),

              ( [ ( 'iron', 1 ), ( 'carbon', 1 ) ],
                [ ( 'steel', 1 ) ] ),

              ( [ ( 'water', 4 ), ( 'mandrake root', 2 ),
                  ( 'valerian root', 2 ), ( 'nightshade', 1 ) ],
                [ ( 'elixir of life', 1 ) ] ),

              ( [ ( 'ethanol', 7 ) ], [ ( 'elixir of life', 1 ) ] ),

              ( [ ( 'chamomile', 3 ), ( 'water', 4 ),
                  ( 'verbena', 1 ), ( 'valerian root', 1 ) ],
                [ ( 'relaxing concoction', 1 ) ] ),

              ( [ ( 'ice', 6 ) ], [ ( 'water', 5 ) ] ),

              ( [ ( 'lead', 10 ), ( 'philosopher stone', 1 ),
                  ( 'unicorn hair', 2 ) ],
                [ ( 'gold', 10 ) ] ),

              ( [ ( 'steel', 3 ) ], [ ( 'cable', 1 ) ] ) ]

    a = alchemy( [ ( 'ethanol', 5 ) ], [ ( 'ethanol', 4 ) ], [] )
    assert a, "avail: 5 ethanol, desired: 4 ethanol"

    a = alchemy( [ ( 'tea leaves', 6 ), ( 'primrose oil', 4 ),
                   ( 'zinc', 2 ), ( 'water', 10 ) ],
                 [ ( 'skin cleaning oil', 1 ) ], rules )
    assert a, "skin cleaning oil, valid"

    # check that we have enough tea leaves after -> we don't
    a = alchemy( [ ( 'tea leaves', 6 ), ( 'primrose oil', 4 ),
                   ( 'zinc', 2 ), ( 'water', 10 ) ],
                 [ ( 'skin cleaning oil', 1 ),
                   ( 'tea leaves', 2 ) ], rules )
    assert not a, "not enough tea tree leaves"

    # check that we have enough tea leaves after -> we do
    a = alchemy( [ ( 'tea leaves', 6 ), ( 'primrose oil', 4 ),
                   ( 'zinc', 2 ), ( 'water', 10 ) ],
                 [ ( 'skin cleaning oil', 1 ),
                   ( 'tea leaves', 1 ) ], rules )
    assert a, "enough tea tree leaves"

    # check that we have enough tea leaves after -> we do
    a = alchemy( [ ( 'tea leaves', 6 ), ( 'primrose oil', 4 ),
                   ( 'zinc', 2 ), ( 'water', 10 ) ],
                 [ ( 'tea leaves', 1 ),
                   ( 'skin cleaning oil', 1 ) ], rules )
    assert a, "enough tea tree leaves, switch order"

    # don't have enough steel as of now but more can be created
    a = alchemy( [ ( 'steel', 2 ), ( 'iron', 2 ), ( 'carbon', 1 ),
                   ( 'footprint', 2 ), ( 'water', 10 ) ],
                 [ ( 'steel', 3 ), ( 'carbon', 2 ) ], rules )
    assert a, "forge steel"

    a = alchemy( [ ( 'nightshade', 1 ), ( 'chamomile', 4 ),
                   ( 'ice', 20 ), ( 'water', 2 ),
                   ( 'verbena', 1 ), ( 'valerian root', 3 ),
                   ( 'ethanol', 9 ), ( 'mandrake root', 2 ) ],
                 [ ( 'elixir of life', 2 ),
                   ( 'relaxing concoction', 1 ) ], rules )
    assert a, "elixirs"

    # no rule to create ice
    a = alchemy( [ ( 'ice', 1 ), ( 'water', 5 ) ],
                 [ ( 'water', 2 ), ( 'ice', 3 ) ], rules )
    assert not a, "no rule to create ice"

    a = alchemy( [ ( 'philosopher stone', 2 ), ( 'tea leaves', 17 ),
                   ( 'unicorn hair', 5 ), ( 'lead', 12 ),
                   ( 'water', 5 ) ],
                 [ ( 'tea tree oil', 3 ), ( 'gold', 11 ) ], rules )
    assert not a, "no ingredients for enough gold"

    a = alchemy( [ ( 'philosopher stone', 2 ), ( 'tea leaves', 17 ),
                   ( 'unicorn hair', 5 ), ( 'lead', 22 ),
                   ( 'water', 5 ) ],
                 [ ( 'tea tree oil', 3 ), ( 'gold', 11 ) ],
                 rules )
    assert a, "enough ingredients"

    a = alchemy( [ ( 'footprint', 4 ), ( 'iron', 3 ),
                   ( 'water', 5 ) ], [ ( 'cable', 1 ) ], rules )
    assert a, "3rd level of indirection"


if __name__ == "__main__":
    test_main()
