from sqlalchemy import create_engine  
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker 

from db_create import engine,engine_backup,engine_backup_for_backup,State_leadership,Fed_leadership,Elected_officials_mid,school_board,state_assem_sena,Fed_Senators,Fed_Representative,Township

def now(data):
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= Township(municipal_name=i["Name"], type_of_municipal=i["type"], District=i["District"], official_name=i["person name"], official_designation=i["designation"], contact_details=i["Contact details"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"


def for_Federal(data):
    
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= Fed_Representative(State=i["State"] ,District=i['District'], Official_name=i["Name"], Party_name=i["Party"], Office_room=i["Office Room"], Phone=i["Phone"], Committee_Assignment=i["Committee Assignment"], Address1=i["Address1"], Address2=i["Address2"], Address3=i["Address3"], Address4=i["Address4"], Address5=i["Address5"], Address6=i["Address6"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"

def for_Federal_Senators(data):
# (self, State, Official_name, Class_of_official, Address, Phone ,Contact_url)

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= Fed_Senators(State=i["State"] ,Class_of_official=i["Class"], Official_name=i["Name"], Phone=i["Contact Number"], Contact_url = i["Conatct URL"], Address=i["Address"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"
# Name,State,Class,Address,Contact Number,Conatct URL


def for_state_sen_assem(data):

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= state_assem_sena(Conunty_name=i["Name"] ,Type=i["type"], Official_name=i["Person name"], Party=i["Party"], District = i["District"], Designation=i["Designation"], Occupation=i["Occupation"], Contact=i["Contact"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"

def State_school_board(data):

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= school_board(Conunty_name_and_code=i["County name(county code)"] ,
            District_and_code=i['Distict name(dist code)'],
            Municipal_name = i["Municipal_name"],
            Address = i['address'],
            Official_one_name=i['official name1'],
            Official_one_title = i['official_title1'],
            Official_one_phone = i['official phone1'],
            Official_one_email = i['official email1'],
            Official_two_name=i['Official Name2'], 
            Official_two_title=i['Official Title2'],
            Official_two_phone_with_ext=i['Official Phone with .ext2'],
            Official_three_name=i['Official Name3'], 
            Official_three_title=i['Official Title3'], 
            Official_three_phone_with_ext=i['Official Phone with .ext3'], 
            Official_four_name=i['Official Name4'], 
            Official_four_title=i['Official Title4'], 
            Official_four_phone_with_ext=i['Official Phone with .ext4'],
            Official_five_name=i['Official Name5'],
            Official_five_title=i['Official Title5'],
            Official_five_phone_with_ext=i['Official Phone with .ext5'],
            Official_six_name=i['Official Name6'],
            Official_six_title=i['Official Title6'], 
            Official_six_phone_with_ext=i['Official Phone with .ext6'],
            Official_seven_name=i['Official Name7'], 
            Official_seven_title=i['Official Title7'],
            Official_seven_phone_with_ext=i['Official Phone with .ext7']
            )
        session.add(d)  
    session.commit()
    session.close()
    print "done"


def for_Elected_officials(data):
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= Elected_officials_mid(County_name=i["Name"], Type=i["type"], Official_name=i["person name"],  Official_designation=i["designation"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"


def for_President_vise(data):

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= Fed_leadership(Name=i["Name"], Age=i['Age'], Designation=i["Designation"], Party = i["Party"], Website_url=i['Website_url'] )  
        session.add(d)  
    session.commit()
    session.close()
    print "done"




def for_gov_lt(data):

    Session = sessionmaker(bind=engine)
    session = Session()

    for i in data:
        d= State_leadership(State=i['State'], Name=i["Name"], Designation=i["Designation"])  
        session.add(d)  
    session.commit()
    session.close()
    print "done"



def move_data_from_main_to_backup():


    Session = sessionmaker(bind=engine)
    Session_backup = sessionmaker(bind=engine_backup)

    session = Session()
    session_backup = Session_backup()

    query = session.query(State_leadership)
    for _row in query.all():

        d= State_leadership(State=_row.State, Name=_row.Name, Designation=_row.Designation)
        session_backup.add(d)
        session_backup.commit()


    query = session.query(Fed_leadership)
    for _row in query.all():

        d= Fed_leadership(Name=_row.Name, Age=_row.Age,Designation= _row.Designation,Party= _row.Party ,Website_url= _row.Website_url)  
        session_backup.add(d)
        session_backup.commit()


    query = session.query(Elected_officials_mid)
    for _row in query.all():

        d= Elected_officials_mid(County_name=_row.County_name,Type= _row.Type, Official_name=_row.Official_name, Official_designation= _row.Official_designation)  
        session_backup.add(d)
        session_backup.commit()


    query = session.query(state_assem_sena)
    for _row in query.all():

        d= state_assem_sena(Conunty_name=_row.Conunty_name,Type=_row.Type,Official_name= _row.Official_name, Party=_row.Party, District=_row.District , Designation=_row.Designation,Occupation= _row.Occupation,Contact= _row.Contact)

        session_backup.add(d)
        session_backup.commit()

    
    query = session.query(Fed_Senators)
    for _row in query.all():

        d= Fed_Senators(State=_row.State, Official_name=_row.Official_name,Class_of_official=_row.Class_of_official, Address=_row.Address, Phone=_row.Phone, Contact_url=_row.Contact_url)

        session_backup.add(d)
        session_backup.commit()



    query = session.query(Fed_Representative)
    for _row in query.all():

        d= Fed_Representative(State=_row.State ,District=_row.District, Official_name=_row.Official_name,Party_name= _row.Party_name,Office_room= _row.Office_room, Phone=_row.Phone, Committee_Assignment=_row.Committee_Assignment, Address1=_row.Address1, Address2=_row.Address2, Address3=_row.Address3, Address4=_row.Address4, Address5=_row.Address5, Address6=_row.Address6)  


        session_backup.add(d)
        session_backup.commit()



    query = session.query(Township)
    for _row in query.all():

        d= Township(municipal_name=_row.municipal_name, type_of_municipal=_row.type_of_municipal, District=_row.District, official_name=_row.official_name, official_designation=_row.official_designation, contact_details=_row.contact_details)  

        session_backup.add(d)
        session_backup.commit()


    query = session.query(school_board)
    for _row in query.all():

        d= school_board(Conunty_name_and_code=_row.Conunty_name_and_code ,
            District_and_code=_row.District_and_code,
            Municipal_name = _row.Municipal_name,
            Address=_row.Address,
            Official_one_name=_row.Official_one_name,
            Official_one_title=_row.Official_one_title,
            Official_one_phone=_row.Official_one_phone,
            Official_one_email=_row.Official_one_email,
            Official_two_name=_row.Official_two_name, 
            Official_two_title=_row.Official_two_title,
            Official_two_phone_with_ext=_row.Official_two_phone_with_ext,
            Official_three_name=_row.Official_three_name, 
            Official_three_title=_row.Official_three_title, 
            Official_three_phone_with_ext=_row.Official_three_phone_with_ext, 
            Official_four_name=_row.Official_four_name, 
            Official_four_title=_row.Official_four_title, 
            Official_four_phone_with_ext=_row.Official_four_phone_with_ext,
            Official_five_name=_row.Official_five_name,
            Official_five_title=_row.Official_five_title,
            Official_five_phone_with_ext=_row.Official_five_phone_with_ext,
            Official_six_name=_row.Official_six_name,
            Official_six_title=_row.Official_six_title, 
            Official_six_phone_with_ext=_row.Official_six_phone_with_ext,
            Official_seven_name=_row.Official_seven_name, 
            Official_seven_title=_row.Official_seven_title,
            Official_seven_phone_with_ext=_row.Official_seven_phone_with_ext
            )
        session_backup.add(d)
        session_backup.commit()
    session.close()
    session_backup.close()





def move_data_from_main__backup_to_backup():


    Session = sessionmaker(bind=engine_backup)
    Session_backup = sessionmaker(bind=engine_backup_for_backup)

    session = Session()
    session_backup = Session_backup()

    query = session.query(State_leadership)
    for _row in query.all():

        d= State_leadership(State=_row.State, Name=_row.Name, Designation=_row.Designation)
        session_backup.add(d)
        session_backup.commit()


    query = session.query(Fed_leadership)
    for _row in query.all():

        d= Fed_leadership(Name=_row.Name, Age=_row.Age,Designation= _row.Designation,Party= _row.Party ,Website_url= _row.Website_url)  
        session_backup.add(d)
        session_backup.commit()


    query = session.query(Elected_officials_mid)
    for _row in query.all():

        d= Elected_officials_mid(County_name=_row.County_name,Type= _row.Type, Official_name=_row.Official_name, Official_designation= _row.Official_designation)  
        session_backup.add(d)
        session_backup.commit()


    query = session.query(state_assem_sena)
    for _row in query.all():

        d= state_assem_sena(Conunty_name=_row.Conunty_name,Type=_row.Type,Official_name= _row.Official_name, Party=_row.Party, District=_row.District , Designation=_row.Designation,Occupation= _row.Occupation,Contact= _row.Contact)

        session_backup.add(d)
        session_backup.commit()

    
    query = session.query(Fed_Senators)
    for _row in query.all():

        d= Fed_Senators(State=_row.State, Official_name=_row.Official_name,Class_of_official=_row.Class_of_official, Address=_row.Address, Phone=_row.Phone, Contact_url=_row.Contact_url)

        session_backup.add(d)
        session_backup.commit()



    query = session.query(Fed_Representative)
    for _row in query.all():

        d= Fed_Representative(State=_row.State ,District=_row.District, Official_name=_row.Official_name,Party_name= _row.Party_name,Office_room= _row.Office_room, Phone=_row.Phone, Committee_Assignment=_row.Committee_Assignment, Address1=_row.Address1, Address2=_row.Address2, Address3=_row.Address3, Address4=_row.Address4, Address5=_row.Address5, Address6=_row.Address6)  


        session_backup.add(d)
        session_backup.commit()



    query = session.query(Township)
    for _row in query.all():

        d= Township(municipal_name=_row.municipal_name, type_of_municipal=_row.type_of_municipal, District=_row.District, official_name=_row.official_name, official_designation=_row.official_designation, contact_details=_row.contact_details)  

        session_backup.add(d)
        session_backup.commit()


    query = session.query(school_board)
    for _row in query.all():

        d= school_board(Conunty_name_and_code=_row.Conunty_name_and_code ,
            District_and_code=_row.District_and_code,
            Municipal_name = _row.Municipal_name,
            Address=_row.Address,
            Official_one_name=_row.Official_one_name,
            Official_one_title=_row.Official_one_title,
            Official_one_phone=_row.Official_one_phone,
            Official_one_email=_row.Official_one_email,
            Official_two_name=_row.Official_two_name, 
            Official_two_title=_row.Official_two_title,
            Official_two_phone_with_ext=_row.Official_two_phone_with_ext,
            Official_three_name=_row.Official_three_name, 
            Official_three_title=_row.Official_three_title, 
            Official_three_phone_with_ext=_row.Official_three_phone_with_ext, 
            Official_four_name=_row.Official_four_name, 
            Official_four_title=_row.Official_four_title, 
            Official_four_phone_with_ext=_row.Official_four_phone_with_ext,
            Official_five_name=_row.Official_five_name,
            Official_five_title=_row.Official_five_title,
            Official_five_phone_with_ext=_row.Official_five_phone_with_ext,
            Official_six_name=_row.Official_six_name,
            Official_six_title=_row.Official_six_title, 
            Official_six_phone_with_ext=_row.Official_six_phone_with_ext,
            Official_seven_name=_row.Official_seven_name, 
            Official_seven_title=_row.Official_seven_title,
            Official_seven_phone_with_ext=_row.Official_seven_phone_with_ext
            )
        session_backup.add(d)
        session_backup.commit()
    session.close()
    session_backup.close()





def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def retrive_data_for_comparison(e,c):
    
    Session = sessionmaker(bind=e)
    session = Session()

    query = session.query(c)
    d = []

    for row in query.all():
        row=row2dict(row)
        d.append(row)
    session.close()
        
    return d



