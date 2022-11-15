from typing import Callable, Any, Protocol

# Below is an implementation of a ‹@record› decorator which can be
# used to create classes that simply keep attributes (records, data
# classes), without having to type out the ‹__init__› method.

# The use case is similar to the ‹dataclass› decorator, but the
# below implementation is much simpler. Default values must always
# be set, and they are shallow-copied into each instance.
# Additionally, the synthetic ‹__init__› method takes an optional
# argument for each attribute, in which case the given attribute is
# initialized to that value, instead of the default.

# Make sure the decorator works as advertised. If not, fix it.

def record( cls: type ) -> type:
    class rec:
        def __init__( self, *args: Any ) -> None:
            from copy import copy
            counter = 0
            for k, v in cls.__dict__.items():
                if not k.startswith( '__' ):
                    if len( args ) > counter:
                        self.__dict__[ k ] = args[ counter ]
                    else:
                        self.__dict__[ k ] = copy( v )
                    counter += 1
    return rec
