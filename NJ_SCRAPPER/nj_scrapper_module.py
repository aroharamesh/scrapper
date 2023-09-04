from custom_scrapper import converter_southbro,southbrunswick,SouthRiver, Spotswood, Milltown, Carteret, Cranbury, Dunellen, EastBrunswick, Edison, Helmetta, HighlandPark, Jamesburg, Middlesex, Monroe, Metuchen, NewBrunswick, NorthBrunswick, OldBridge, PerthAmboy, Piscataway, Plainsboro, Sayreville, SouthAmboy, SouthRiver, Woodbridge, SouthPlainfield, Federal, state_senate_assembly, ElectedOfficials, prasident_and_vise, govr_and_ltgov

from db_module.db_create import Base,engine_backup,engine,engine_backup_for_backup

from db_module import push_data

from Comparison_module import compare

import ack_mail

import time

try:
    import httplib
except:
    import http.client as httplib
import schedule
import time

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def Council():
	

	Carteret.Process("http://www.carteret.net/content/2855/3390/default.aspx", "Council","Borough"," Carteret","Council","19")
	Cranbury.Process("http://cranburytownship.org/twp_committee.html", "Council","Township","Cranbury","Council",'14')
	Dunellen.Process("http://www.dunellen-nj.gov/government/mayor_and_council/index.php#.Wk3loN-Wa01", "Council","Borough","Dunellen","Council","22")
	EastBrunswick.Process("https://www.eastbrunswick.org/content/202/293/default.aspx", "Council","Township","East Brunswick","Council",'18')
	Edison.Process("http://www.edisonnj.org/departments/council/council_members.php", "Council","Township","Edison","Council","18")
	Helmetta.Process("http://www.helmettaboro.com/Cit-e-Access/TownCouncil/?TID=102&TPID=10557", "Council","Borough","Helmetta","Council",'18')
	HighlandPark.Process("http://www.hpboro.com/Directory.aspx?DID=32", "Council","Borough","Highland Park","Council",'18')
	Jamesburg.Process("http://www.jamesburgborough.org/boroughcouncil.html", "Council","Township","Jamesburg","Council",'14')
	Metuchen.Process("http://www.metuchennj.org/metnj/GOVERNMENT/Borough%20Council/", "Council","Borough","Metuchen","Council",'18')
	Middlesex.Process("http://www.middlesexboro-nj.gov/index.php/get-involved/contact-us", "Council","Borough","Middlesex","Council",'22')
	Milltown.Process("http://www.milltownnj.org/municipal/", "Council","Township","Milltown","Council",'17') 
	Monroe.Process("http://www.monroetwp.com/township_council.cfm", "Council","Township","Monroe","Council",'14')
	NewBrunswick.Process("http://thecityofnewbrunswick.org/city-council/","Council","City","New Brunswick","Council",'17')
	NorthBrunswick.Process("http://www.northbrunswicknj.gov/mayor-council/council", "Council","Township","North Brunswick ","Council",'17')
	OldBridge.Process("http://www.oldbridge.com/content/5144/5243/default.aspx", "Council","Township","Oldbridge","Council","12")
	PerthAmboy.Process("http://ci.perthamboy.nj.us/", "Council","City","Perth Amboy","Council",'19')
	Piscataway.Process("http://www.piscatawaynj.org/admin_dept/mayor-township-council", "Council","Township","Piscataway","Council",'17')
	Plainsboro.Process("http://www.plainsboronj.com/309/Mayor-Township-Committee", "Council","Township","Plainsboro","Council",'14')
	Sayreville.Process("http://www.sayreville.com/Cit-e-Access/TownCouncil/?TID=87&TPID=8636", "Council","Borough","Sayreville","Council","19")
	southbrunswick.Process("http://www.southbrunswicknj.gov/directory", "Council","Township","South Brunswick","Council",'16')
	SouthPlainfield.Process("http://www.southplainfieldnj.com/spnj/Mayor%20%26%20Council/", "Council","Borough","South Plainfield","Council",'18')
	SouthRiver.Process("http://www.southrivernj.org/elected_officials.html", "Council","Borough","South River","Council","18")
	Spotswood.Process("http://www.spotswoodboro.com/council.html", "Council","Township","Spotswood","Council",'14') 
	Woodbridge.Process("http://www.twp.woodbridge.nj.us/340/Council", "Council","Township","Woodbridge","Council","19")

	      



def fed_san_cong():
	Federal.Congressmen()
	Federal.Senators_of_the_115th_Congress()



def sta_senate_assembly():
	state_senate_assembly.Process("http://www.njleg.state.nj.us/districts/districtnumbers.asp", "county","Middlesex","Middlesex","county")



def school_board_state():
	Federal.New_Jersey_School_Directory()


def Elected_Officials():
	ElectedOfficials.Process("http://www.middlesexcountynj.gov/Government/ElectedOfficials/Pages/default.aspx", "ElectedOfficials","County","Middlesex","ElectedOfficials")


def leadership():
	prasident_and_vise.prasident_and_vise()



def state_leadership():
	govr_and_ltgov.Gov_Ltgov()


def compare_data():
	import os
	import json

	wd = os.getcwd()

	resultset= compare()

	ack = []
	for i in resultset:
	    for key, value in i.iteritems():
	        ack.append(value)

	if ack.count('There is no change in data')==8:
	    print 'No Change in the data,Thank You'
	    try:
	    	ack_mail.success_mail()
	    except Exception as e:
	    	print str(e)

	    
	else:
		with open(os.path.join(os.path.join(wd,"error_obj"),'ticket_details.json'), 'w') as outfile:
			json.dump(resultset, outfile)
		try:
			ack_mail.eroor_mail()
		except Exception as e:
			print str(e)
		print 'Data Has changed , sending an acknoldgement email to predefined Emails,Thank You '




def job():

	start = time.time()

	if  have_internet()== True:
		print 'drop backup for backup'
		Base.metadata.drop_all(engine_backup_for_backup)
		print 'drop backup for backup'
		print '====================================================='
		print 'craete backup for backup'
		Base.metadata.create_all(engine_backup_for_backup)
		print 'craete backup'
		print '====================================================='
		print 'Move'
		push_data.move_data_from_main__backup_to_backup()
		print 'Move'



		print 'drop backup'
		Base.metadata.drop_all(engine_backup)
		print 'drop backup'
		print '====================================================='
		print 'craete backup'
		Base.metadata.create_all(engine_backup)
		print 'craete backup'
		print '====================================================='
		print 'Move'
		push_data.move_data_from_main_to_backup()
		print 'Move'
		print '====================================================='

		
		print 'drop main'
		Base.metadata.drop_all(engine)
		print 'drop main'
		print '====================================================='
		print 'craete main'
		Base.metadata.create_all(engine)
		print 'craete main'
		print '====================================================='

		Council()
		fed_san_cong()
		sta_senate_assembly()
		school_board_state()
		Elected_Officials()
		leadership()
		state_leadership()
		compare_data()

		end = time.time()
		# print
		print "Last Execution started at: %s"%(start)
		print "Last Execution ended at: %s"%(end)
		print "Last Execution Completed in: %s"%(end - start)

	else:
		print 'No intenet connection, sending an acknoldgement email to predefined Emails,Thank You '


schedule.every(1500).minutes.do(job)


while True:
	
	schedule.run_pending()
	time.sleep(1)


