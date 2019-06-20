
"""
Custom Exceptions I raise. I catch these in the Main.py and handle them all differently
"""
class NFCScanError(Exception):
    pass

class CancelError(Exception):
    pass

class UserError(Exception):
    pass

class ApiError(Exception):
    pass