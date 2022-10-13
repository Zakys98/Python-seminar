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
#    ‹date_of_entry›, ‹species› and ‹breed›, plus ‹adoption_date›,
#    where:
#
#    ◦ the date of entry is a ‹datetime.date› instance,
#    ◦ ‹year_of_birth› is an integer,
#    ◦ everything else is a string,
#    ◦ ‹name›, ‹species› and ‹date_of_entry› are required, the rest
#      is optional,
#    ◦ ‹adoption_date› can be set in cases where an animal is being
#      added retroactively and is equivalent to calling ‹adopt› (see
#      below) atomically,
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
#      ‹date› is a ‹datetime.date› instance, and returns an object
#      representing the exam, with attributes corresponding to the
#      keyword arguments,
#    ◦ method ‹list_exams› which takes keyword arguments ‹start› and
#      ‹end›, both ‹datetime.date› instances, or ‹None› (the range is
#      inclusive; in the latter case, the range is not limited in
#      that direction),
#    ◦ method ‹adopt› which takes keyword arguments ‹date› (a
#      ‹datetime.date› instance) and optionally ‹adopter_name› and
#      ‹adopter_address› which are strings,
#    ◦ method ‹start_foster› which takes a ‹date› (again a
#      ‹datetime.date› instance), ‹parent› (which accepts one of
#      the objects returned by ‹available_foster_parents› listed
#      below) and an optional ‹end_date› (for cases when the
#      fostering is recorded retroactively),
#    ◦ ‹end_foster› which takes a ‹date›,
#
#  • ‹add_foster_parent› which accepts keyword arguments ‹name›,
#    ‹address› and ‹phone_number› (all strings) and ‹max_animals›
#    which is an ‹int› and returns the object representing the
#    foster parent,
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
#    in foster care on the given date, or ‹start_foster› is called
#    without an ‹end_date› on a date that predates an existing
#    fostering record, or ‹start_foster› is called with an
#    ‹end_date› that overlaps an existing fostering record,
#  • attempting to adopt an animal that was in foster care on that
#    day, or attempting to put an animal that has been adopted
#    on that or earlier day into foster care, or was not at the
#    shelter that day at all for some other reason,
#  • attempting to do a veterinary exam on an animal which is in
#    foster care or already adopted at the time (however, exams can
#    be performed on the same day as fostering is started or ended,
#    or on the day of adoption),
#  • an attempt is made to exceed the capacity of a foster parent,
#  • adoption of an animal that has already been adopted is
#    attempted (regardless of dates),
#  • adoption of an animal at a date that predates a recorded
#    veterinary exam (i.e. the exam record would be rendered invalid
#    by the adoption),
#  • to avoid confusion, an action is prevented if it would cause
#    two animals with the same name and species to be housed by the
#    shelter at the same time (it is still an error even if they
#    would never meet due to fostering – an animal of the same name
#    & species can only be accepted into the shelter after the first
#    was adopted; of course, having ‘Jesenius’ and ‘Jesenius II’ at
#    the same time is perfectly acceptable).

from datetime import date
from typing import Optional


class Person:
    def __init__(self, name: str, address: Optional[str]) -> None:
        self.name = name
        self.address = address


class Adopter(Person):
    def __init__(self, name: str, address: Optional[str]) -> None:
        super().__init__(name, address)


class FosterParent(Person):
    def __init__(self, name: str, address: str, phone_number: str, max_animals: int) -> None:
        super().__init__(name, address)
        self.phone_number = phone_number
        self.max_animals = max_animals
        self.foster_cares: list[FosterCare] = []

    def is_under_max_limit(self, date: date) -> bool:
        count = 0
        for care in self.foster_cares:
            if care.end is None:
                if care.start <= date:
                    count += 1
            elif care.start <= date and care.end >= date:
                count += 1
        return True if count < self.max_animals else False


class FosterCare:
    def __init__(self, start: date, parent: FosterParent, end: Optional[date]) -> None:
        self.start = start
        self.end: Optional[date] = end
        self.parent = parent


class Exam:
    def __init__(self, vet: str, date: date, report: str) -> None:
        self.vet = vet
        self.date = date
        self.report = report


class Animal:
    def __init__(self, name: str, date_of_entry: date, species: str, year_of_birth: Optional[int] = None,
                 gender: Optional[str] = None, breed: Optional[str] = None, date_of_adopt: Optional[date] = None) -> None:
        self.name = name
        self.year_of_birth = year_of_birth
        self.gender = gender
        self.date_of_entry = date_of_entry
        self.species = species
        self.breed = breed
        self.exams: list[Exam] = []
        self.foster_cares: list[FosterCare] = []
        self.adopter: Optional[Adopter] = None
        self.date_of_adopt: Optional[date] = date_of_adopt

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Animal):
            return False
        if self.name == __o.name and self.species == __o.species:
            if __o.date_of_adopt is None:
                if self.date_of_adopt is None:
                    return True
                if self.date_of_adopt is not None and __o.date_of_entry <= self.date_of_adopt:
                    return True
            else:
                if __o.date_of_adopt >= self.date_of_entry and (self.date_of_adopt is None or self.date_of_adopt >= __o.date_of_entry):
                    return True
                if self.date_of_adopt is not None \
                   and self.date_of_adopt < __o.date_of_adopt and \
                   self.date_of_adopt > __o.date_of_entry:
                    return True
        return False

    def add_exam(self, vet: str, date: date, report: str) -> Exam:
        for foster_care in self.foster_cares:
            if foster_care.end is None:
                if foster_care.start < date:
                    raise RuntimeError
            elif foster_care.start < date and foster_care.end > date:
                raise RuntimeError
        if self.date_of_adopt is not None and self.date_of_adopt <= date:
            raise RuntimeError
        exam = Exam(vet, date, report)
        self.exams.append(exam)
        return exam

    def list_exams(self, start: Optional[date], end: Optional[date]) -> list[Exam]:
        if start is None and end is None:
            return self.exams
        if start is None and end is not None:
            return [exam for exam in self.exams if exam.date <= end]
        if start is not None and end is None:
            return [exam for exam in self.exams if exam.date >= start]
        if start is not None and end is not None:
            return [exam for exam in self.exams if exam.date >= start and exam.date <= end]
        return []

    def _check_foster_care(self, date: date) -> None:
        if self.is_in_foster_care(date):
            raise RuntimeError

    def is_in_foster_care(self, date: date) -> bool:
        for foster_care in self.foster_cares:
            if foster_care.end is None:
                if foster_care.start <= date:
                    return True
            elif foster_care.start <= date and foster_care.end >= date:
                return True
        return False

    # TODO udelat kontrolu mezi date_of_entry a year_of_birth
    def adopt(self, date: date, adopter_name: Optional[str] = None, adopter_address: Optional[str] = None) -> None:
        self._check_foster_care(date)
        for foster in self.foster_cares:
            if foster.start > date:
                raise RuntimeError
        for exam in self.exams:
            if exam.date >= date:
                raise RuntimeError
        if self.date_of_adopt is not None or self.date_of_entry > date: #or self.year_of_birth > date.year \
            raise RuntimeError
        if adopter_name is not None:
            self.adopter = Adopter(adopter_name, adopter_address)
        self.date_of_adopt = date

    def start_foster(self, date: date, parent: FosterParent, end_date: Optional[date] = None) -> None:
        self._check_foster_care(date)
        if end_date is not None:
            self._check_foster_care(end_date)
            for foster in self.foster_cares:
                if foster.end is not None and foster.start >= date and foster.end <= end_date:
                    raise RuntimeError
        else:
            for foster in self.foster_cares:
                if foster.end is None:
                    raise RuntimeError
        if self.date_of_adopt is not None:
            if self.date_of_adopt <= date:
                raise RuntimeError
            if end_date is not None and self.date_of_adopt <= end_date:
                raise RuntimeError
        if not parent.is_under_max_limit(date):
            raise RuntimeError
        foster_care = FosterCare(date, parent, end_date)
        parent.foster_cares.append(foster_care)
        self.foster_cares.append(foster_care)

    def end_foster(self, date: date) -> None:
        for foster in self.foster_cares:
            if foster.end is None:
                foster.end = date
                return
        raise RuntimeError


class Shelter:
    def __init__(self) -> None:
        self.animals: list[Animal] = []
        self.foster_parents: list[FosterParent] = []

    def add_animal(self, name: str, date_of_entry: date, species: str, year_of_birth: Optional[int] = None, gender: Optional[str] = None,
                   breed: Optional[str] = None, adoption_date: Optional[date] = None) -> Animal:
        animal = Animal(name=name, date_of_entry=date_of_entry, species=species,
                        year_of_birth=year_of_birth, gender=gender, breed=breed, date_of_adopt=adoption_date)
        if animal in self.animals:
            raise RuntimeError
        self.animals.append(animal)
        return animal

    def list_animals(self, date: date, name: Optional[str] = None, year_of_birth: Optional[int] = None,
                     gender: Optional[str] = None, date_of_entry: Optional[date] = None,
                     species: Optional[str] = None, breed: Optional[str] = None) -> list[Animal]:
        output = []
        for animal in self.animals:
            if name is not None and name != animal.name:
                continue
            if year_of_birth is not None and year_of_birth != animal.year_of_birth:
                continue
            if gender is not None and gender != animal.gender:
                continue
            if date_of_entry is not None and date_of_entry != animal.date_of_entry:
                continue
            if species is not None and species != animal.species:
                continue
            if breed is not None and breed != animal.breed:
                continue
            if animal.date_of_entry > date:
                continue
            if animal.is_in_foster_care(date):
                continue
            if animal.date_of_adopt is not None and animal.date_of_adopt < date:
                continue
            output.append(animal)
        return output

    def add_foster_parent(self, name: str, address: str, phone_number: str, max_animals: int) -> FosterParent:
        foster_parent = FosterParent(
            name, address, phone_number, max_animals)
        self.foster_parents.append(foster_parent)
        return foster_parent

    def available_foster_parents(self, date: date) -> list[FosterParent]:
        output = []
        for parent in self.foster_parents:
            if parent.is_under_max_limit(date):
                output.append(parent)
        return output
