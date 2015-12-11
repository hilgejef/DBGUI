###############################################################################
# ResultStatus
#
# Object containing query result data			
#	
###############################################################################

class ResultStatus():
    def __init__(self, success = True, message = None, data = None):
        self.Success = success
        self.Message = message
        self.Data = data