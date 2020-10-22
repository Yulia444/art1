import random
from functools import reduce
import re
import weakref

MAX_ITEMS = 11
MAX_CUSTOMERS = 10
TOTAL_PROTOTYPE_VECTORS = 5

BETA = 1.0  
VIGILANCE = 0.9  
DATABASE = []
PROTOTYPES = []

VERBOSITY = False

customers = [[0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]]


def bit_wise_and(v1, v2):
    return Vector([item[0] & item[1] for item in zip(v1, v2)])


class Vector(list):
    __instances = list()

    def __init__(self, init=None, rand=False):
        if not init:
            if rand:
                self.init = [random.randint(0, 1) for _ in range(MAX_ITEMS)]
            else:
                self.init = [0] * MAX_ITEMS

            super(Vector, self).__init__(self.init)
        else:
            self.init = init
            super(Vector, self).__init__(self.init)
        Vector.__instances.append(weakref.ref(self))

    def __eq__(self, other):
        return self.id == other.id

    @property
    def magn(self):
        """
        magnitude
        """
        for i in self:
            assert i <= 1

        return float(sum(self))
    
    """
    @classmethod
    def getinstances(cls):
        dead = list()
        for ref in cls.__instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.append(ref())
        
        cls.__instances = [item for item in cls.__instances if item not in dead]

    @classmethod
    def deleteinstances(cls):
        for obj in cls.getinstances():
            del obj

    """

    
class Prototype(Vector):
    _id = 0
    __instances = list()

    def __init__(self, customer):
        Prototype._id += 1
        self.id = self._id
        super(Prototype, self).__init__(list(customer))
        self.customers = []
        self.changed = False
        self.add_customer(customer)
        Prototype.__instances.append(weakref.ref(self))

    def __repr__(self):
        l = super(Prototype, self).__repr__()
        return "Prototype vector {}: {}".format(self.id, l)

    def add_customer(self, customer):
        if customer.cluster and customer.cluster == self:
            return

        if customer.cluster:
            customer.cluster.remove_customer(customer)

        self.customers.append(customer)
        customer.cluster = self
        self.update()

    def remove_customer(self, customer):
        self.customers.remove(customer)
        customer.cluster = None

        if not self.customers:
            PROTOTYPES.remove(self)
        else:
            self.update()

    def update(self):
        v = zip(*self.customers)

        for i, row in enumerate(v):
            self[i] = reduce(lambda a, b: a & b, row)

    @property
    def sum_vector(self):
        v = zip(*self.customers)
        return [sum(item) for item in v]


class Customer(Vector):
    _id = 0
    __instances = []

    def __init__(self, *args, **kwargs):
        Customer._id += 1
        self.id = self._id
        super(Customer, self).__init__(*args, **kwargs)
        self.cluster = None
        Customer.__instances.append(weakref.ref(self))
    

    def __repr__(self):
        l = super(Customer, self).__repr__()
        return "Customer {}: {}".format(self.id, l)

    def recomedation(self):
        if not self.cluster:
            return None

        max_val = -1
        recomedation = []

        for i, item in enumerate(self.cluster.sum_vector):
            if not self[i]:
                if item > max_val:
                    max_val = item
                    recomedation = [i]
                elif item == max_val:
                    recomedation.append(i)

        return recomedation


def clusters_to_string(customers):
    string = ""
    for customer, id in zip(customers, [id for id in range(1, len(customers)+1)]):
        string += "Customer {}:\t {}".format(id, " ".join([str(i) for i in customer])) + '\n'
    return string


def string_to_clasters(string):
    cluster_matches = re.findall(r"Customer\s\d{1,}:\s{1,}((0|1|\s){1,})", string)
    clusters = []
    for match in cluster_matches:
        clusters.append([int(i) for i in match[0].strip('\n').split(' ')])
    return clusters


def init(string=None, customers=None):
    if string:
        customers = string_to_clasters(string)
    elif customers:
        customers = customers

    for customer in customers:
        DATABASE.append(Customer(init=customer))


def performART1():
    done = False
    count = 50

    while not done:
        done = True

        for customer in DATABASE:

            for prototype in PROTOTYPES:
                if customer.cluster and customer.cluster == prototype:
                    continue

                and_result = bit_wise_and(customer, prototype)
                result = and_result.magn / (BETA + prototype.magn)
                test = customer.magn / (BETA + MAX_ITEMS)

                
                if result > test:
         
                    if and_result.magn / customer.magn < VIGILANCE:
                        if customer.cluster and VERBOSITY:
                            print('Customer {} moved from cluster {} to {}'.format(
                                customer.id, customer.cluster.id, prototype.id))
                        elif VERBOSITY:
                            print('Customer {} appended to cluster {}'.format(
                                customer.id, prototype.id))

                        done = False
                        prototype.add_customer(customer)

        
            if not customer.cluster:
                done = False
                if len(PROTOTYPES) < TOTAL_PROTOTYPE_VECTORS:
                    if VERBOSITY:
                        print('Created new cluster for customer {}'.format(customer.id))
                    new_prototype = Prototype(customer)
                    PROTOTYPES.append(new_prototype)

        count -= 1
        if count <= 0:
            break


if __name__ == "__main__":
    customers = [[0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
             [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]]
    init(customers=customers)
    performART1()

    for prototype in PROTOTYPES:
        print(prototype)
        for customer in prototype.customers:
            print(customer)
        print()
