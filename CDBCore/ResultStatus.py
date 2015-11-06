###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/5/2015
# Date Modified:	11/5/2015
# File Name:		ResultStatus.py
#
# Overview:
#	Provides a standardized framework for passing results within the
#	application.  Data includes:
#
#		Success: Boolean value indicating success or failure
#		Message: The error message if failure.
#		Data:	 Any data that the result contains.
#
###############################################################################

class ResultStatus():
    def __init__(self, success = True, message = None, data = None):
        self.Success = success
        self.Message = message
        self.Data = data