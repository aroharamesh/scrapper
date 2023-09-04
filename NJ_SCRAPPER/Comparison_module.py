
from deepdiff import DeepDiff  # For Deep Difference of 2 objects

from deepdiff import DeepSearch  # For finding if item exists in an object
from db_module.db_create import engine,engine_backup,State_leadership,Fed_leadership,Elected_officials_mid,school_board,state_assem_sena,Fed_Senators,Fed_Representative,Township
from sqlalchemy.orm import sessionmaker	
from db_module.push_data import retrive_data_for_comparison
def compare_now(d,dd):
	item1 = d
	item2 = dd
	return DeepDiff(item1,item2,ignore_order=True)

def compare_data(d,dd):
		

	a =  len(compare_now(d,dd))
	if a==0:
		return 'There is no change in data'
	else:
		return compare_now(d,dd)


def  compare():
	result = []

	class_name_string="State_leadership,Fed_leadership,Elected_officials_mid,school_board,state_assem_sena,Fed_Senators,Fed_Representative,Township"
	for i in class_name_string.split(','):

		d=retrive_data_for_comparison(engine,eval(i))
		dd=retrive_data_for_comparison(engine_backup,eval(i))
		result.append({i:compare_data(d,dd)})
	return result





