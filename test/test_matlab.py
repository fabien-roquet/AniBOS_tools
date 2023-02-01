from AniBOS_tools.matlab import matlab_dataclass


matlab = matlab_dataclass()
eng = matlab.matlab_engine


print('pwd =',eng.pwd())
eng.workspace['EXP'] = 'ct107'
eng.workspace['one_smru_name'] = 'ct107-933-13'
print('EXP =',eng.workspace['EXP'])
print('one_smru_name =',eng.workspace['one_smru_name'])
matlab.stop_matlab()
