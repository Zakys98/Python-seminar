# You volunteer for a local animal shelter, and they really need to
# get more organized. Since you are a programmer, you decide to step
# up to the job and write a small information system for them. Here is
# what it needs to do:
#
#  • track all the resident animals and their basic stats: name, year
#    of birth, gender, date of entry, species and breed,
#  • store veterinary records: animals undergo exams, each of which
#    has a date, the name of the attending vet and a text report,
#  • record periods of foster care: animals can be moved out of the
#    shelter, into the care of individuals for a period of time –
#    record the start and end date of each instance, along with the
#    foster parent,
#  • for each prospective foster parent, keep the name, address,
#    phone number and the number of animals they can keep at once,
#  • record adoptions: when was which animal adopted and by whom,
#  • keep the name and address of each adopter.
#
# In the remainder of the spec, we will make full use of «duck
# typing»: for each entity, we will only specify the interface, the
# exact classes and their relationships are up to you, as long as
# they provide the required methods and attributes. The only class
# given by name is ‹Shelter›, which is the entry point of the whole
# system.
#
# The ‹Shelter› class needs to provide the following methods:
#
#  • ‹add_animal› which accepts keyword arguments for each of the
#    basic stats listed above: ‹name›, ‹year_of_birth›, ‹gender›,
#    ‹date_of_entry›, ‹species› and ‹breed›, where:
#
#    ◦ the date of entry is a ‹datetime.date› instance,
#    ◦ ‹year_of_birth› is an integer,
#    ◦ everything else is a string,
#
#    and returns the object representing the animal (see
#    ‹list_animals› below for details about its interface),
#
#  • ‹list_animals› which accepts:
#
#    ◦ optional keyword arguments for each of the basic stats: only
#      animals that match all the criteria (their corresponding
#      attribute is equal to the value supplied to ‹list_animals›,
#      «if» it was supplied) should be listed,
#    ◦ a ‹date› keyword argument: only animals which were possibly
#      present in the shelter at this time (i.e. were not adopted on
#      an earlier date, and were not in foster care that entire day)
#      should be listed;
#
#    The elements of the list returned by ‹list_animals› should have:
#
#    ◦ each of the basic stats as an attribute of the corresponding
#      type (see ‹add_animal›),
#    ◦ method ‹add_exam› which accepts keyword arguments ‹vet› and
#      ‹date› and ‹report›, where ‹vet› and ‹report› are strings and
#      ‹date› is a ‹datetime.date› instance,
#    ◦ method ‹list_exams› which takes keyword arguments ‹start› and
#      ‹end›, both ‹datetime.date› instances, or ‹None› (the range is
#      inclusive; in the latter case, the range is not limited in
#      that direction),
#    ◦ method ‹adopt› which takes keyword arguments ‹date› (a
#      ‹datetime.date› instance) and ‹adopter_name› and
#      ‹adopter_address› which are strings,
#    ◦ method ‹start_foster› which takes a ‹date› (again a
#      ‹datetime.date› instance) and ‹parent›, which accepts one of
#      the objects returned by ‹available_foster_parents› listed
#      below,
#    ◦ ‹end_foster› which takes a ‹date›,
#
#  • ‹add_foster_parent› which accepts keyword arguments ‹name›,
#    ‹address› and ‹phone_number› (all strings) and ‹max_animals›
#    which is an ‹int›,
#
#  • ‹available_foster_parents› which takes a keyword argument ‹date›
#    and lists foster parents with free capacity at this date (i.e.
#    those who can keep more animals than they are or were keeping at
#    the given date – if an animal is taken or returned on a given
#    date, it still counts into the limit).
#
# Raise a ‹RuntimeError› in (at least) these cases:
#
#  • ‹start_foster› was called on an animal that was already in foster
#    care at the given date, or ‹end_foster› on an animal that was not
#    in foster care at the given date,
#  • attempting to adopt an animal that was in foster care on that
#    day, or attempting to put an animal that has been adopted
#    on that or earlier day into foster care,
#  • attempting to do a veterinary exam on an animal which is in
#    foster care or already adopted at the time (however, exams can
#    be performed on the same day as fostering is started or ended,
#    or on the day of adoption),
#  • an attempt is made to exceed the capacity of a foster parent.

class Animal:
    def __init__(self) -> None:
        pass

class Shelter:
    def __init__(self) -> None:
        pass

    def add_animal(self):
        pass

    def list_animals(self):
        pass

    def add_foster_parent(self):
        pass

    def available_foster_parents(self):
        pass

