import json

import numpy as np
from ravcom import dump_data, RavQueue, QUEUE_LOW_PRIORITY, QUEUE_HIGH_PRIORITY
from ravcom import globals as g
from ravcom import ravdb

from ravop.enums import *


def epsilon():
    return Scalar(1e-07)


def one():
    return Scalar(1)


def minus_one():
    return Scalar(-1)


def inf():
    return Scalar(np.inf)


def pi():
    return Scalar(np.pi)


class Op(object):
    def __init__(self, id=None,
                 operator=None, inputs=None, outputs=None, **kwargs):
        self._op_db = None

        if id is not None:
            self._op_db = ravdb.get_op(op_id=id)
            if self._op_db is None:
                raise Exception("Invalid op id")
        else:
            if (inputs is not None or outputs is not None) and operator is not None:
                self._op_db = self.create(operator=operator, inputs=inputs, outputs=outputs, **kwargs)
            else:
                raise Exception("Invalid parameters")

    def wait(self):
        self._op_db = ravdb.refresh(self._op_db)
        while self._op_db.status != "computed" or self._op_db.status != "failed":
            pass

    def create(self, operator, inputs=None, outputs=None, **kwargs):
        if (inputs is not None or outputs is not None) and operator is not None:
            # Figure out node type
            if inputs is None and outputs is not None:
                node_type = NodeTypes.INPUT.value
            elif inputs is not None and outputs is None:
                node_type = NodeTypes.MIDDLE.value
            else:
                raise Exception("Invalid node type")

            if inputs is not None:
                if len(inputs) == 1:
                    op_type = OpTypes.UNARY.value
                elif len(inputs) == 2:
                    op_type = OpTypes.BINARY.value
                else:
                    raise Exception("Invalid number of inputs")
            else:
                op_type = OpTypes.OTHER.value

            if outputs is None:
                status = OpStatus.PENDING.value
            else:
                status = OpStatus.COMPUTED.value

            inputs = json.dumps(inputs)
            outputs = json.dumps(outputs)

            op = ravdb.create_op(name=kwargs.get("name", None),
                                 graph_id=g.graph_id,
                                 node_type=node_type,
                                 inputs=inputs,
                                 outputs=outputs,
                                 op_type=op_type,
                                 operator=operator,
                                 status=status,
                                 params=json.dumps(kwargs))
            # Add op to queue
            if op.status != OpStatus.COMPUTED.value and op.status != OpStatus.FAILED.value:
                if g.graph_id is None:
                    q = RavQueue(name=QUEUE_HIGH_PRIORITY)
                    q.push(op.id)
                else:
                    q = RavQueue(name=QUEUE_LOW_PRIORITY)
                    q.push(op.id)

            return op
        else:
            raise Exception("Invalid parameters")

    # Arithmetic
    def lin(self, **kwargs):
        return lin(self, **kwargs)

    def add(self, op, **kwargs):
        return add(self, op, **kwargs)

    def sub(self, op, **kwargs):
        return sub(self, op, **kwargs)

    def mul(self, op, **kwargs):
        return mul(self, op, **kwargs)

    def div(self, op, **kwargs):
        return div(self, op, **kwargs)

    def pos(self, **kwargs):
        return pos(self, **kwargs)

    def neg(self, **kwargs):
        return neg(self, **kwargs)

    def exp(self, **kwargs):
        return exp(self, **kwargs)

    def natlog(self, **kwargs):
        return natlog(self, **kwargs)

    def pow(self, op, **kwargs):
        return pow(self, op, **kwargs)

    def square(self, **kwargs):
        return square(self, **kwargs)

    def cube(self, **kwargs):
        return cube(self, **kwargs)

    def square_root(self, **kwargs):
        return square_root(self, **kwargs)

    def cube_root(self, **kwargs):
        return cube_root(self, **kwargs)

    def abs(self, **kwargs):
        return abs(self, **kwargs)

    # Matrix
    def matmul(self, op, **kwargs):
        return matmul(self, op, **kwargs)

    def multiply(self, op, **kwargs):
        return multiply(self, op, **kwargs)

    def dot(self, op, **kwargs):
        return dot(self, op, **kwargs)

    def transpose(self, **kwargs):
        return transpose(self, **kwargs)

    def sum(self, **kwargs):
        return sum(self, **kwargs)

    def sort(self, **kwargs):
        return sort(self, **kwargs)

    def split(self, **kwargs):
        return split(self, **kwargs)

    def reshape(self, **kwargs):
        return reshape(self, **kwargs)

    def concat(self, op, **kwargs):
        return concat(self, op, **kwargs)

    def min(self, **kwargs):
        return min(self, **kwargs)

    def max(self, **kwargs):
        return max(self, **kwargs)

    def unique(self, **kwargs):
        return unique(self, **kwargs)

    def argmax(self, **kwargs):
        return argmax(self, **kwargs)

    def argmin(self, **kwargs):
        return argmin(self, **kwargs)

    def expand_dims(self, **kwargs):
        return expand_dims(self, **kwargs)

    def inv(self, **kwargs):
        return inv(self, **kwargs)

    def gather(self, op, **kwargs):
        return gather(self, op, **kwargs)

    def reverse(self, **kwargs):
        return reverse(self, **kwargs)

    def stack(self, **kwargs):
        return stack(self, **kwargs)

    def tile(self, **kwargs):
        return tile(self, **kwargs)

    def slice(self, **kwargs):
        return slice(self, **kwargs)

    def find_indices(self, op, **kwargs):
        return find_indices(self, op, **kwargs)

    def shape_(self, **kwargs):
        return shape(self, **kwargs)

    # Comparison Ops
    def greater(self, op1, **kwargs):
        return greater(self, op1, **kwargs)

    def greater_equal(self, op1, **kwargs):
        return greater_equal(self, op1, **kwargs)

    def less(self, op1, **kwargs):
        return less(self, op1, **kwargs)

    def less_equal(self, op1, **kwargs):
        return less_equal(self, op1, **kwargs)

    def equal(self, op1, **kwargs):
        return equal(self, op1, **kwargs)

    def not_equal(self, op1, **kwargs):
        return not_equal(self, op1, **kwargs)

    # Logical
    def logical_and(self, op1, **kwargs):
        return logical_and(self, op1, **kwargs)

    def logical_or(self, op1, **kwargs):
        return logical_or(self, op1, **kwargs)

    def logical_not(self, **kwargs):
        return logical_not(self, **kwargs)

    def logical_xor(self, op1, **kwargs):
        return logical_xor(self, op1, **kwargs)

    # Statistical
    def mean(self, **kwargs):
        return mean(self, **kwargs)

    def average(self, **kwargs):
        return average(self, **kwargs)

    def mode(self, **kwargs):
        return mode(self, **kwargs)

    def median(self, **kwargs):
        return median(self, **kwargs)

    def variance(self, **kwargs):
        return variance(self, **kwargs)

    def std(self, **kwargs):
        return std(self, **kwargs)

    def percentile(self, **kwargs):
        return percentile(self, **kwargs)

    def random(self, **kwargs):
        return random(self, **kwargs)

    def bincount(self, **kwargs):
        return bincount(self, **kwargs)

    def where(self, op1, **kwargs):
        return where(self, op1, **kwargs)

    def sign(self, **kwargs):
        return sign(self, **kwargs)

    def foreach(self, **kwargs):
        return foreach(self, **kwargs)

    def to_tensor(self):
        return Tensor(id=self.id)
        # self._op_db = ravdb.refresh(self._op_db)
        # if self._op_db.outputs is None or self._op_db.outputs == "null":
        #     return None
        #
        # data_id = json.loads(self._op_db.outputs)[0]
        # data = Data(id=data_id)
        # return Tensor(data.value)

    def to_scalar(self):
        self._op_db = ravdb.refresh(self._op_db)
        if self._op_db.outputs is None or self._op_db.outputs == "null":
            return None

        data_id = json.loads(self._op_db.outputs)[0]
        data = Data(id=data_id)
        return Scalar(data.value)

    @property
    def output(self):
        self._op_db = ravdb.refresh(self._op_db)
        if self._op_db.outputs is None or self._op_db.outputs == "null":
            return None

        data_id = json.loads(self._op_db.outputs)[0]
        data = Data(id=data_id)
        return data.value

    @property
    def output_dtype(self):
        self._op_db = ravdb.refresh(self._op_db)
        if self._op_db.outputs is None or self._op_db.outputs == "null":
            return None

        data_id = json.loads(self._op_db.outputs)[0]
        data = Data(id=data_id)
        return data.dtype

    @property
    def id(self):
        return self._op_db.id

    @property
    def status(self):
        self._op_db = ravdb.refresh(self._op_db)
        return self._op_db.status

    def __str__(self):
        return "Op:\nId:{}\nName:{}\nType:{}\nOperator:{}\nOutput:{}\nStatus:{}\n".format(self.id, self._op_db.name,
                                                                                          self._op_db.op_type,
                                                                                          self._op_db.operator,
                                                                                          self.output,
                                                                                          self.status)

    def __call__(self, *args, **kwargs):
        return self.output

    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __mul__(self, other):
        return mul(self, other)

    def __pos__(self):
        return pos(self)

    def __neg__(self):
        return neg(self)

    def __abs__(self):
        return abs(self)

    def __invert__(self):
        return inv(self)

    def __lt__(self, other):
        return less(self, other)

    def __le__(self, other):
        return less_equal(self, other)

    def __eq__(self, other):
        return equal(self, other)

    def __ne__(self, other):
        return not_equal(self, other)

    def __ge__(self, other):
        return greater_equal(self, other)


class Scalar(Op):
    def __init__(self, value, **kwargs):
        # 1. Store it in a file
        # 2. Create data object
        # 3. Create data op

        # Find dtype
        self._dtype = None
        self.__find_dtype(value)

        data = Data(value=value, dtype=self.dtype)
        super().__init__(operator=Operators.LINEAR.value, inputs=None, outputs=[data.id], **kwargs)

    def __find_dtype(self, x):
        if type(x).__name__ == "str":
            x = json.loads(x)
            if type(x).__name__ == "int":
                self._dtype = "int"
            elif type(x).__name__ == "float":
                self._dtype = "float"
            elif type(x).__name__ == "list":
                raise Exception("Invalid data")
            else:
                raise Exception("Invalid value")

        elif type(x).__name__ == "int":
            self._dtype = "int"
        elif type(x).__name__ == "float":
            self._dtype = "float"
        elif type(x).__name__ == "list":
            raise Exception("Invalid data")

    @property
    def dtype(self):
        return self._dtype

    def __str__(self):
        return "Scalar Op:\nId:{}\nOutput:{}\nStatus:{}\nDtype:{}\n".format(self.id, self.output,
                                                                            self.status, self.dtype)

    def __call__(self, *args, **kwargs):
        return self.output


class Tensor(Op):
    """
    It supports:
    1. list
    2. ndarray
    3. string(list)
    """

    def __init__(self, value, **kwargs):
        # 1. Store it in a file
        # 2. Create data object
        # 3. Create data op
        """
        Kwargs
        1.db
        2.name
        3.graph
        """
        if type(value).__name__ == "list":
            value = np.array(value)
        elif type(value).__name__ == "str":
            x = json.loads(value)
            if type(x).__name__ == "list":
                value = np.array(value)

        self._shape = value.shape

        data = Data(value=value, dtype="ndarray")
        super().__init__(operator=Operators.LINEAR.value, inputs=None, outputs=[data.id], **kwargs)

    @property
    def dtype(self):
        return "ndarray"

    @property
    def shape(self):
        return self._shape

    def __str__(self):
        return "Tensor Op:\nId:{}\nOutput:{}\nStatus:{}\nDtype:{}\n".format(self.id, self.output,
                                                                            self.status, self.dtype)

    def __call__(self, *args, **kwargs):
        return self.output


class Data(object):
    def __init__(self, id=None, value=None, dtype=None, **kwargs):
        self._data_db = None

        if id is not None:
            self._data_db = ravdb.get_data(data_id=id)
            if self._data_db is None:
                raise Exception("Invalid data id")

        elif value is not None and dtype is not None:

            if type(value).__name__ == "list":
                value = np.array(value)
            elif type(value).__name__ == "str":
                x = json.loads(value)
                if type(x).__name__ == "list":
                    value = np.array(value)

            self._data_db = self.__create(value=value, dtype=dtype)
            if self._data_db is None:
                raise Exception("Unable to create data")

    def __create(self, value, dtype):
        data = ravdb.create_data(type=dtype)

        if dtype == "ndarray":
            file_path = dump_data(data.id, value)
            # Update file path
            ravdb.update_data(data, file_path=file_path)
        elif dtype in ["int", "float"]:
            ravdb.update_data(data, value=value)

        return data

    @property
    def value(self):
        self._data_db = ravdb.refresh(self._data_db)
        if self.dtype == "ndarray":
            file_path = self._data_db.file_path
            value = np.load(file_path, allow_pickle=True)
            return value
        elif self.dtype in ["int", "float"]:
            if self.dtype == "int":
                return int(self._data_db.value)
            elif self.dtype == "float":
                return float(self._data_db.value)

    @property
    def id(self):
        return self._data_db.id

    @property
    def dtype(self):
        self._data_db = ravdb.refresh(self._data_db)
        return self._data_db.type

    def __str__(self):
        return "Data:\nId:{}\nDtype:{}\n".format(self.id, self.dtype)

    def __call__(self, *args, **kwargs):
        return self.value


class Graph(object):
    """A class to represent a graph object"""

    def __init__(self, id=None, **kwargs):
        if id is None and g.graph_id is None:
            # Create a new graph
            self._graph_db = ravdb.create_graph()
            g.graph_id = self._graph_db.id
        elif id is not None:
            # Get an existing graph
            self._graph_db = ravdb.get_graph(graph_id=id)
        elif g.graph_id is not None:
            # Get an existing graph
            self._graph_db = ravdb.get_graph(graph_id=g.graph_id)

        # Raise an exception if there is no graph created
        if self._graph_db is None:
            raise Exception("Invalid graph id")

    def add(self, op):
        """Add an op to the graph"""
        op.add_to_graph(self._graph_db)

    @property
    def id(self):
        return self._graph_db.id

    @property
    def status(self):
        self._graph_db = ravdb.refresh(self._graph_db)
        return self._graph_db.status

    @property
    def progress(self):
        """Get the progress"""
        stats = self.get_op_stats()
        if stats['total_ops'] == 0:
            return 0
        progress = ((stats["computed_ops"] + stats["computing_ops"] + stats["failed_ops"]) / stats["total_ops"]) * 100
        return progress

    def get_op_stats(self):
        """Get stats of all ops"""
        ops = ravdb.get_graph_ops(graph_id=self.id)

        pending_ops = 0
        computed_ops = 0
        computing_ops = 0
        failed_ops = 0

        for op in ops:
            if op.status == "pending":
                pending_ops += 1
            elif op.status == "computed":
                computed_ops += 1
            elif op.status == "computing":
                computing_ops += 1
            elif op.status == "failed":
                failed_ops += 1

        total_ops = len(ops)
        return {"total_ops": total_ops, "pending_ops": pending_ops,
                "computing_ops": computing_ops, "computed_ops": computed_ops,
                "failed_ops": failed_ops}

    def clean(self):
        ravdb.delete_graph_ops(self._graph_db.id)

    @property
    def ops(self):
        ops = ravdb.get_graph_ops(self.id)
        return [Op(id=op.id) for op in ops]

    def print_ops(self):
        """Print ops"""
        for op in self.ops:
            print(op)

    def get_ops_by_name(self, op_name, graph_id=None):
        ops = ravdb.get_ops_by_name(op_name=op_name, graph_id=graph_id)
        return [Op(id=op.id) for op in ops]

    def __str__(self):
        return "Graph:\nId:{}\nStatus:{}\n".format(self.id, self.status)


# Functional Interface of RavOp


# Arithmetic
def lin(op, **kwargs):
    return __create_math_op2(op, Operators.LINEAR.value, **kwargs)


def add(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.ADDITION.value, **kwargs)


def sub(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.SUBTRACTION.value, **kwargs)


def mul(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.MULTIPLICATION.value, **kwargs)


def div(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.DIVISION.value, **kwargs)


def pos(op, **kwargs):
    return __create_math_op2(op, Operators.POSITIVE.value, **kwargs)


def neg(op, **kwargs):
    return __create_math_op2(op, Operators.NEGATION.value, **kwargs)


def exp(op, **kwargs):
    return __create_math_op2(op, Operators.EXPONENTIAL.value, **kwargs)


def natlog(op, **kwargs):
    return __create_math_op2(op, Operators.NATURAL_LOG.value, **kwargs)


def pow(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.POWER.value, **kwargs)


def square(op1, **kwargs):
    return __create_math_op2(op1, Operators.SQUARE.value, **kwargs)


def cube(op1, **kwargs):
    return __create_math_op2(op1, Operators.CUBE.value, **kwargs)


def square_root(op1, **kwargs):
    return __create_math_op2(op1, Operators.SQUARE_ROOT.value, **kwargs)


def cube_root(op1, **kwargs):
    return __create_math_op2(op1, Operators.CUBE_ROOT.value, **kwargs)


def abs(op1, **kwargs):
    return __create_math_op2(op1, Operators.ABSOLUTE.value, **kwargs)


# Tensors
def matmul(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.MATRIX_MULTIPLICATION.value, **kwargs)


def multiply(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.MULTIPLY.value, **kwargs)


def dot(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.DOT.value, **kwargs)


def transpose(op, **kwargs):
    return __create_math_op2(op, Operators.TRANSPOSE.value, **kwargs)


def sum(op, **kwargs):
    return __create_math_op2(op, Operators.MATRIX_SUM.value, **kwargs)


def sort(op, **kwargs):
    return __create_math_op2(op, Operators.SORT.value, **kwargs)


def split(op, **kwargs):
    return __create_math_op2(op, Operators.SPLIT.value, **kwargs)


def reshape(op, **kwargs):
    return __create_math_op2(op, Operators.RESHAPE.value, **kwargs)


def concat(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.CONCATENATE.value, **kwargs)


def min(op1, **kwargs):
    return __create_math_op2(op1, Operators.MIN.value, **kwargs)


def max(op1, **kwargs):
    return __create_math_op2(op1, Operators.MAX.value, **kwargs)


def unique(op1, **kwargs):
    return __create_math_op2(op1, Operators.UNIQUE.value, **kwargs)


def argmax(op1, **kwargs):
    return __create_math_op2(op1, Operators.ARGMAX.value, **kwargs)


def argmin(op1, **kwargs):
    return __create_math_op2(op1, Operators.ARGMIN.value, **kwargs)


def expand_dims(op, **kwargs):
    return __create_math_op2(op, Operators.EXPAND_DIMS.value, **kwargs)


def inv(op, **kwargs):
    return __create_math_op2(op, Operators.INVERSE.value, **kwargs)


def gather(op, op2, **kwargs):
    return __create_math_op(op, op2, Operators.GATHER.value, **kwargs)


def reverse(op, **kwargs):
    return __create_math_op2(op, Operators.REVERSE.value, **kwargs)


def stack(op, **kwargs):
    return __create_math_op2(op, Operators.STACK.value, **kwargs)


def tile(op, **kwargs):
    return __create_math_op2(op, Operators.TILE.value, **kwargs)


def slice(op, **kwargs):
    return __create_math_op2(op, Operators.SLICE.value, **kwargs)


def find_indices(op, op2, **kwargs):
    return __create_math_op(op, op2, Operators.FIND_INDICES.value, **kwargs)


def shape(op, **kwargs):
    return __create_math_op2(op, Operators.SHAPE.value, **kwargs)


# Comparison
def greater(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.GREATER.value, **kwargs)


def greater_equal(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.GREATER_EQUAL.value, **kwargs)


def less(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.LESS.value, **kwargs)


def less_equal(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.LESS_EQUAL.value, **kwargs)


def equal(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.EQUAL.value, **kwargs)


def not_equal(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.NOT_EQUAL.value, **kwargs)


# Logical
def logical_and(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.LOGICAL_AND.value, **kwargs)


def logical_or(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.LOGICAL_OR.value, **kwargs)


def logical_not(op1, **kwargs):
    return __create_math_op2(op1, Operators.LOGICAL_NOT.value, **kwargs)


def logical_xor(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.LOGICAL_XOR.value, **kwargs)


# Statistical
def mean(op1, **kwargs):
    return __create_math_op2(op1, Operators.MEAN.value, **kwargs)


def average(op1, **kwargs):
    return __create_math_op2(op1, Operators.AVERAGE.value, **kwargs)


def mode(op1, **kwargs):
    return __create_math_op2(op1, Operators.MODE.value, **kwargs)


def median(op1, **kwargs):
    return __create_math_op2(op1, Operators.MEDIAN.value, **kwargs)


def variance(op1, **kwargs):
    return __create_math_op2(op1, Operators.VARIANCE.value, **kwargs)


def std(op1, **kwargs):
    return __create_math_op2(op1, Operators.STANDARD_DEVIATION.value, **kwargs)


def percentile(op1, **kwargs):
    return __create_math_op2(op1, Operators.PERCENTILE.value, **kwargs)


def random(op1, **kwargs):
    return __create_math_op2(op1, Operators.RANDOM.value, **kwargs)


def bincount(op1, **kwargs):
    return __create_math_op2(op1, Operators.BINCOUNT.value, **kwargs)


def where(op1, op2, **kwargs):
    return __create_math_op(op1, op2, Operators.WHERE.value, **kwargs)


def sign(op1, **kwargs):
    return __create_math_op2(op1, Operators.SIGN.value, **kwargs)


def foreach(op, **kwargs):
    return __create_math_op2(op, Operators.FOREACH.value, **kwargs)


# Data Preprocessing


def one_hot_encoding(op, **kwargs):
    return __create_math_op2(op, Operators.ONE_HOT_ENCODING.value, **kwargs)


def __create_math_op(op1, op2, operator, **kwargs):
    if op1 is None or op2 is None:
        raise Exception("Null Op")

    params = dict()
    for key, value in kwargs.items():
        if isinstance(value, Op) or isinstance(value, Data) or isinstance(value, Scalar) or isinstance(value, Tensor):
            params[key] = value.id
        elif type(value).__name__ in ['int', 'float']:
            params[key] = Scalar(value).id
        elif isinstance(value, list) or isinstance(value, tuple):
            params[key] = Tensor(value).id
        elif type(value).__name__ == 'str':
            params[key] = value

    op = ravdb.create_op(name=kwargs.get('name', None),
                         graph_id=g.graph_id,
                         node_type=NodeTypes.MIDDLE.value,
                         inputs=json.dumps([op1.id, op2.id]),
                         outputs=json.dumps(None),
                         op_type=OpTypes.BINARY.value,
                         operator=operator,
                         status=OpStatus.PENDING.value,
                         params=json.dumps(params))

    # Add op to queue
    if op.status != OpStatus.COMPUTED.value and op.status != OpStatus.FAILED.value:
        if g.graph_id is None:
            q = RavQueue(name=QUEUE_HIGH_PRIORITY)
            q.push(op.id)
        else:
            q = RavQueue(name=QUEUE_LOW_PRIORITY)
            q.push(op.id)

    return Op(id=op.id)


def __create_math_op2(op1, operator, **kwargs):
    if op1 is None:
        raise Exception("Null Op")

    params = dict()
    for key, value in kwargs.items():
        if isinstance(value, Op) or isinstance(value, Data) or isinstance(value, Scalar) or isinstance(value, Tensor):
            params[key] = value.id
        elif type(value).__name__ in ['int', 'float']:
            params[key] = Scalar(value).id
        elif isinstance(value, list) or isinstance(value, tuple):
            params[key] = Tensor(value).id
        elif type(value).__name__ == 'str':
            params[key] = value

    op = ravdb.create_op(name=kwargs.get('name', None),
                         graph_id=g.graph_id,
                         node_type=NodeTypes.MIDDLE.value,
                         inputs=json.dumps([op1.id]),
                         outputs=json.dumps(None),
                         op_type=OpTypes.UNARY.value,
                         operator=operator,
                         status=OpStatus.PENDING.value,
                         params=json.dumps(params))

    # Add op to queue
    if op.status != OpStatus.COMPUTED.value and op.status != OpStatus.FAILED.value:
        if g.graph_id is None:
            q = RavQueue(name=QUEUE_HIGH_PRIORITY)
            q.push(op.id)
        else:
            q = RavQueue(name=QUEUE_LOW_PRIORITY)
            q.push(op.id)

    from ravcom import inform_server
    inform_server()

    return Op(id=op.id)
