# define Python user-defined exceptions

class BitcoinException(Exception):
   """Base class for other exceptions"""
   pass

class InsufficientBalanceException(BitcoinException):
   """Raised when the input value is too large"""
   pass

class AmountTooLargeException(BitcoinException):
   """Raised when the input value is too large"""
   pass
