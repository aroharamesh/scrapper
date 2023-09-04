from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


# engine = create_engine("mssql+pymssql://sa:123@localhost/njscrapper",  pool_recycle=3600,echo=True)

# engine_backup = create_engine("mssql+pymssql://sa:123@localhost/njscrapper_backup", echo=True)
# '''
engine = create_engine("postgresql://idia:postgres@postgres.cvc8b2isrkrv.us-west-2.rds.amazonaws.com/njscrapper", echo=True)
# 
engine_backup = create_engine("postgresql://idia:postgres@postgres.cvc8b2isrkrv.us-west-2.rds.amazonaws.com/njscrapper_backup", echo=True)

engine_backup_for_backup = create_engine("postgresql://idia:postgres@postgres.cvc8b2isrkrv.us-west-2.rds.amazonaws.com/njscrapper_backup_backup", echo=True)
# '''
# engine = create_engine("postgresql://postgres:123@localhost/njscrapper", echo=True, pool_pre_ping=True)

# engine_backup = create_engine("postgresql://postgres:123@localhost/njscrapper_backup", echo=True, pool_pre_ping=True)



Base = declarative_base()

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


#--------------------------------------------------------------------------------------------
class Township(Base):
    __tablename__ = "Township"
    id = Column(Integer,primary_key=True) #primary_key=True
    municipal_name = Column(String(100))
    type_of_municipal = Column(String(100))
    District = Column(String(100))
    official_name = Column(String(100))
    official_designation = Column(String(100))
    contact_details = Column(String(500))
    

    def __init__(self, municipal_name, type_of_municipal, District, official_name, official_designation, contact_details):
        self.municipal_name = municipal_name
        self.type_of_municipal = type_of_municipal
        self.District = District
        self.official_name = official_name
        self.official_designation = official_designation
        self.contact_details = contact_details

#--------------------------------------------------------------------------------------------
class Fed_Representative(Base):
    __tablename__ = "Fed_Representative"
    id = Column(Integer,primary_key=True) #primary_key=True
    State = Column(String(100))
    District = Column(String(100))
    Official_name = Column(String(100))
    Party_name = Column(String(100))
    Office_room = Column(String(100))
    Phone = Column(String(100))
    Committee_Assignment= Column(String(100))
    Address1= Column(String(500))
    Address2= Column(String(500))
    Address3= Column(String(500))
    Address4= Column(String(500))
    Address5= Column(String(500))
    Address6= Column(String(500))


    def __init__(self, State,District, Official_name, Party_name, Office_room, Phone ,Committee_Assignment, Address1, Address2, Address3, Address4, Address5, Address6):
        self.State = State
        self.District = District
        self.Official_name = Official_name
        self.Party_name = Party_name
        self.Office_room = Office_room
        self.Phone = Phone
        self.Committee_Assignment= Committee_Assignment
        self.Address1 = Address1
        self.Address2 = Address2
        self.Address3 = Address3
        self.Address4 = Address4
        self.Address5 = Address5
        self.Address6 = Address6

#--------------------------------------------------------------------------------------------
class Fed_Senators(Base):
    __tablename__ = "Fed_Senators"
    id = Column(Integer,primary_key=True) #primary_key=True
    State = Column(String(100))
    Official_name = Column(String(100))
    Class_of_official = Column(String(100))
    Address= Column(String(500))
    Phone= Column(String(100))
    Contact_url= Column(String(500))
    


    def __init__(self, State, Official_name, Class_of_official, Address, Phone ,Contact_url):
        self.State = State
        self.Official_name = Official_name
        self.Class_of_official = Class_of_official
        self.Address = Address
        self.Phone = Phone
        self.Contact_url= Contact_url
        
#--------------------------------------------------------------------------------------------

class state_assem_sena(Base):
    __tablename__ = "state_assem_sena"
    id = Column(Integer,primary_key=True) #primary_key=True
    Conunty_name = Column(String(100))
    Type = Column(String(100))
    Official_name = Column(String(100))
    Party = Column(String(100))
    District = Column(String(100))
    Designation = Column(String(100))
    Occupation= Column(String(500))
    # Phone= Column(String(100))
    Contact= Column(String(500))
    


    def __init__(self, Conunty_name, Type, Official_name,  Party, District, Designation ,Occupation, Contact):
        self.Conunty_name = Conunty_name
        self.Type = Type
        self.Official_name = Official_name
        self.Party = Party
        self.District = District
        self.Designation= Designation
        self.Occupation = Occupation
        self.Contact= Contact
        



class school_board(Base):
    __tablename__ = "school_board"
    id = Column(Integer,primary_key=True) #primary_key=True
    Conunty_name_and_code = Column(String(100))
    District_and_code = Column(String(100))
    Municipal_name = Column(String(100))
    Address = Column(String(500))
    
    Official_one_name = Column(String(100))
    Official_one_title =  Column(String(100))
    Official_one_phone = Column(String(100))
    Official_one_email = Column(String(100))

    Official_two_name = Column(String(100))
    Official_two_title =  Column(String(100))
    Official_two_phone_with_ext = Column(String(100))
 
    Official_three_name = Column(String(100))
    Official_three_title =  Column(String(100))
    Official_three_phone_with_ext = Column(String(100))

    Official_four_name = Column(String(100))
    Official_four_title =  Column(String(100))
    Official_four_phone_with_ext = Column(String(100))

    Official_five_name = Column(String(100))
    Official_five_title =  Column(String(100))
    Official_five_phone_with_ext = Column(String(100))

    Official_six_name = Column(String(100))
    Official_six_title =  Column(String(100))
    Official_six_phone_with_ext = Column(String(100))

    Official_seven_name = Column(String(100))
    Official_seven_title =  Column(String(100))
    Official_seven_phone_with_ext = Column(String(100))
    


    def __init__(self, Conunty_name_and_code, District_and_code, Municipal_name, Address, Official_one_name, Official_one_title, Official_one_phone, Official_one_email, Official_two_name, Official_two_title, Official_two_phone_with_ext, Official_three_name, Official_three_title, Official_three_phone_with_ext, Official_four_name, Official_four_title, Official_four_phone_with_ext, Official_five_name, Official_five_title, Official_five_phone_with_ext, Official_six_name, Official_six_title, Official_six_phone_with_ext, Official_seven_name, Official_seven_title, Official_seven_phone_with_ext):
        self.Conunty_name_and_code = Conunty_name_and_code
        self.District_and_code = District_and_code
        self.Municipal_name = Municipal_name
        self.Address = Address

        self.Official_one_name = Official_one_name
        self.Official_one_title = Official_one_title
        self.Official_one_phone = Official_one_phone
        self.Official_one_email = Official_one_email

        self.Official_two_name = Official_two_name
        self.Official_two_title = Official_two_title
        self.Official_two_phone_with_ext = Official_two_phone_with_ext

        self.Official_three_name = Official_three_name
        self.Official_three_title = Official_three_title
        self.Official_three_phone_with_ext = Official_three_phone_with_ext

        self.Official_four_name = Official_four_name
        self.Official_four_title = Official_four_title
        self.Official_four_phone_with_ext = Official_four_phone_with_ext 

        self.Official_five_name = Official_five_name
        self.Official_five_title = Official_five_title
        self.Official_five_phone_with_ext = Official_five_phone_with_ext

        self.Official_six_name = Official_six_name
        self.Official_six_title = Official_six_title
        self.Official_six_phone_with_ext = Official_six_phone_with_ext

        self.Official_seven_name = Official_seven_name
        self.Official_seven_title = Official_seven_title
        self.Official_seven_phone_with_ext = Official_seven_phone_with_ext
    
#---------------------------------------------------------------------------------------------

class Elected_officials_mid(Base):
    __tablename__ = "Elected_officials"
    id = Column(Integer,primary_key=True) 
    County_name = Column(String(100))
    Type = Column(String(100))
    Official_name = Column(String(100))
    Official_designation = Column(String(100))

    

    def __init__(self,County_name, Type, Official_name, Official_designation ):
        self.County_name = County_name
        self.Type = Type
        # self.District = District
        self.Official_name = Official_name
        self.Official_designation = Official_designation
        # self.contact_details = contact_details

#----------------------------------------------------------------------------------------------------

class Fed_leadership(Base):
    __tablename__ = "Fed_leadership"
    id = Column(Integer,primary_key=True) 
    Name = Column(String(100))
    Age = Column(String(100))
    Designation = Column(String(100))
    Party = Column(String(100))
    Website_url = Column(String(100))

    

    def __init__(self, Name, Age, Designation, Party, Website_url):
        self.Name = Name
        self.Age = Age
        # self.District = District
        self.Designation = Designation
        self.Party = Party
        self.Website_url = Website_url


#----------------------------------------------------------------------------------------------------------

class State_leadership(Base):
    __tablename__ = "State_leadership"
    id = Column(Integer,primary_key=True) 
    State=Column(String(100))
    Name = Column(String(100))
    Designation = Column(String(100))



    

    def __init__(self, State, Name, Designation):
        self.Name = Name
        self.State = State
        # self.District = District
        self.Designation = Designation


# Base.metadata.drop_all(engine)
# Base.metadata.drop_all(engine_backup)
# Base.metadata.drop_all(engine_backup_for_backup)

# Base.metadata.create_all(engine)
# Base.metadata.create_all(engine_backup)
# Base.metadata.create_all(engine_backup_for_backup)









    
