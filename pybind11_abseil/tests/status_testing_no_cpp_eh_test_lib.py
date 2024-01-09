"""This is a py_library to enable testing with pybind11 & PyCLIF."""

# This is the default for py_test code:
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from absl.testing import absltest
from absl.testing import parameterized

# Exercises status_from_core_py_exc.cc:StatusFromFetchedExc()
TAB_StatusFromFetchedExc = (
    (MemoryError, 'RESOURCE_EXHAUSTED: MemoryError'),
    (NotImplementedError, 'UNIMPLEMENTED: NotImplementedError'),
    (KeyboardInterrupt, 'ABORTED: KeyboardInterrupt'),
    (SystemError, 'INTERNAL: SystemError'),
    (SyntaxError, 'INTERNAL: SyntaxError'),
    (TypeError, 'INVALID_ARGUMENT: TypeError'),
    (ValueError, 'OUT_OF_RANGE: ValueError'),
    (LookupError, 'NOT_FOUND: LookupError'),
    (RuntimeError, 'UNKNOWN: RuntimeError'),
)


class StatusReturnTest(parameterized.TestCase):

  def setUp(self):
    super().setUp()
    self.tm = self.getTestModule()  # pytype: disable=attribute-error

  def testStatusOk(self):  # pylint: disable=invalid-name
    def cb():
      pass

    self.assertEqual(self.tm.CallCallbackWithStatusReturn(cb), 'OK')

  @parameterized.parameters(*TAB_StatusFromFetchedExc)
  def testStatusFromFetchedExc(self, etype, expected):  # pylint: disable=invalid-name

    def cb():
      raise etype('Msg.')

    self.assertEqual(
        self.tm.CallCallbackWithStatusReturn(cb), expected + ': Msg.'
    )

  def testStatusWrongReturnType(self):  # pylint: disable=invalid-name
    def cb():
      return ['something']

    if getattr(self.tm, '__pyclif_codegen_mode__', None) == 'c_api':
      expected = 'OK'
    else:
      expected = (
          'INVALID_ARGUMENT: Unable to cast Python instance of type <class'
          " 'list'> to C++ type 'absl::Status'"
      )
    self.assertEqual(self.tm.CallCallbackWithStatusReturn(cb), expected)

  def testAssertionErrorBare(self):  # pylint: disable=invalid-name

    def cb():
      assert False

    self.assertEqual(
        self.tm.CallCallbackWithStatusReturn(cb), 'UNKNOWN: AssertionError: '
    )

  def testAssertionErrorWithValue(self):  # pylint: disable=invalid-name

    def cb():
      assert False, 'Unexpected'

    self.assertEqual(
        self.tm.CallCallbackWithStatusReturn(cb),
        'UNKNOWN: AssertionError: Unexpected',
    )

  def testErrorStatusNotOkRoundTrip(self):  # pylint: disable=invalid-name

    def cb():
      self.tm.GenerateErrorStatusNotOk()

    self.assertEqual(
        self.tm.CallCallbackWithStatusReturn(cb),
        'ALREADY_EXISTS: Something went wrong, again.',
    )


class StatusOrReturnTest(parameterized.TestCase):

  def setUp(self):
    super().setUp()
    self.tm = self.getTestModule()  # pytype: disable=attribute-error

  def testStatusOrIntOk(self):  # pylint: disable=invalid-name
    def cb():
      return 5

    self.assertEqual(self.tm.CallCallbackWithStatusOrIntReturn(cb), '5')

  @parameterized.parameters(*TAB_StatusFromFetchedExc)
  def testStatusOrIntFromFetchedExc(self, etype, expected):  # pylint: disable=invalid-name
    def cb():
      raise etype('Msg.')

    self.assertEqual(
        self.tm.CallCallbackWithStatusOrIntReturn(cb), expected + ': Msg.'
    )

  def testStatusOrIntWrongReturnType(self):  # pylint: disable=invalid-name
    def cb():
      return '5'

    if getattr(self.tm, '__pyclif_codegen_mode__', None) == 'c_api':
      expected = 'INVALID_ARGUMENT: TypeError: expecting int'
    else:
      expected = (
          'INVALID_ARGUMENT: Unable to cast Python instance of type <class'
          " 'str'> to C++ type 'absl::StatusOr<int>'"
      )
    self.assertEqual(self.tm.CallCallbackWithStatusOrIntReturn(cb), expected)


class StatusOrPyObjectPtrTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.tm = self.getTestModule()  # pytype: disable=attribute-error

  def testStatusOrObject(self):  # pylint: disable=invalid-name
    if getattr(self.tm, '__pyclif_codegen_mode__', None) != 'c_api':
      self.skipTest('TODO(cl/578064081)')
    # No leak (manually verified under cl/485274434).
    while True:
      lst = [1, 2, 3, 4]

      def cb():
        return lst

      # call many times to be sure that object reference is not being removed
      for _ in range(10):
        res = self.tm.CallCallbackWithStatusOrObjectReturn(cb)
        self.assertListEqual(res, lst)
        self.assertIs(res, lst)
      return  # Comment out for manual leak checking (use `top` command).
