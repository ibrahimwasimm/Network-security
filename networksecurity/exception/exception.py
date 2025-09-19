import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        #error message
        self.error_message=error_message,

        #exc_info is built it function and give three(type, value, traceback) values but rn i need only one thats why i used _,_,
        _,_,my_trace=error_details.exc_info()

        self.line_no=my_trace.tb_lineno
        self.file_name=my_trace.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.line_no, str(self.error_message))
        
if __name__=='__main__':
    try:
       logger.logging.info("enter into division error")
       a=1/0
       print("this will not be printed :")
    except Exception as e:
       raise NetworkSecurityException(e,sys)