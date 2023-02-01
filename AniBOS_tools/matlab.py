from matlab import engine
import io
from dataclasses import dataclass

#--------------------  MATLAB  ----------------------------#

@dataclass
class matlab_dataclass:

    # pointer to matlab engine
    matlab_engine: engine.matlabengine.MatlabEngine = None

    def stop_matlab(self):
        self.matlab_engine.quit()
        print('Matlab stopped')
        
    def print_matlab(self, namevar: str):
        with io.StringIO() as out:
            self.matlab_engine.eval(namevar,nargout=0,stdout=out,stderr=out)
            print(out.getvalue())
            
    def run_command(self, cmd: str,verbose=True) -> bool:
        # execute a matlab command
        with io.StringIO() as out, io.StringIO() as err:
            try:
                print(cmd)
                self.matlab_engine.eval(cmd,nargout=0,stdout=out,stderr=err)
                if verbose:
                    print(out.getvalue())
                return True
            except:
                if verbose:
                    print(err.getvalue())
                return False
            
    def get_var(self, var_name: str) -> object:
        return self.matlab_engine.workspace[var_name]

    def __init__(self):
        try:
            self.matlab_engine = engine.start_matlab()
        except engine.EngineError:
            raise Exception("Matlab could not be started")



# Execute in terminal command line
if __name__ == "__main__":

    matlab = matlab_dataclass()
    print(matlab.matlab_engine.pwd())
    matlab.stop_matlab()
                

        

