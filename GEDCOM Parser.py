import os
import sqlite3
import sys
import PrettyTable

dbName = "GEDCOM.db"

tagRules =[
	(0, 'INDI'),
	(1, 'NAME'),
	(1, 'SEX'),
	(1, 'BIRT'),
	(1, 'DEAT'),
	(1, 'FAMC'),
	(1, 'FAMS'),
	(0, 'FAM'),
	(1, 'MARR'),
	(1, 'HUSB'),
	(1, 'WIFE'),
	(1, 'CHIL'),
	(1, 'DIV'),
	(2, 'DATE'),
	(0, 'HEAD'),
	(0, 'TRLR'),
	(0, 'NOTE')
]

# if a file name was passed in
if len(sys.argv) > 1:

	indID = ""
	name = ""
	gender = ""
	birth = ""
	death = "N/A"

	famID = ""
	husband = ""
	wife = ""
	child = ""
	married = ""
	divorced = "N/A"

	lastTag = None

	# loop through lines
	for line in open(sys.argv[1]):

		valid = False
		level = -1
		tag = None
		args = None

		# make sure this line has at least a level and a tag
		words = line.split()
		if len(words) >= 2:

			# level is always first
			level = int(words[0])

			# flag for INDI and FAM
			badOrder = False

			# order is switched for INDI and FAM
			if (len(words) >= 3 and
				(words[2] == 'INDI' or words[2] == 'FAM')):

				tag = words[2]
				args = " ".join([words[1]] + words[3:])
			else:
				tag = words[1]
				args = " ".join(words[2:])

				# INDI and FAM should have been found in block above
				# if this trips, the order is wrong
				if tag == 'INDI' or tag == 'FAM':
					badOrder = True

			# guilty until proven innocent
			valid = False

			# if we find a matching tag rule, and the level checks out
			# tag is valid
			if not badOrder:
				for tagRule in tagRules:
					if tagRule[1]==tag and tagRule[0]==level:
						valid = True

			if (tag == 'NAME'):
				name = args
			elif (tag == 'SEX'):
				gender = args[0]
			elif (lastTag == 'BIRT' and tag == 'DATE'):
				birth = args
			elif (lastTag == 'DEAT' and tag == 'DATE'):
				birth = args

		#prints indiviual's info into table
		if (valid and level == 0):

			#Table for individuals
			INDI_tbl = PrettyTable()
			INDI_tbl.fieldnames = ["ID","Name"]

			INDI_tbl.add_row([name, gender, birth, death])
			print(INDI_tbl)

		#prints familiy	info into table
		if (tag == 'HUSB'):
				husband = args
			elif (tag == 'WIFE'):
				wife = args
			elif (tag == 'CHIL'):
				child = args
			elif (lastTag == 'MARR' and tagg == 'DATE'):
				married = args
			elif (lastTag == 'DIV' and tag == 'DATE'):
				divorced = args

		if (valid and level == 0):

			#Table for families
			FAM_tbl = PrettyTable()
			FAM_tbl.fieldnames = ["Family ID","Husband Name","Husband ID","Wife Name","Wife ID"]

			FAM_tbl.add_row([famID, husband, wife])
			print(FAM_tbl)

def dbInit():

	try:
		os.remove(dbName);
	except FileNotFoundError:
		pass

	conn = sqlite3.connect(dbName)
	curs = conn.cursor()

	curs.execute('''CREATE TABLE individuals (
		id 			TEXT	NOT NULL	PRIMARY KEY,
		firstName	TEXT	NOT NULL,
		lastName 	TEXT	NOT NULL,
		gender 		TEXT	NOT NULL,
		birth 		DATE	NOT NULL,
		death 		DATE,

		CHECK (gender in ("M", "F"))
	)''')

	curs.execute('''CREATE TABLE families (
		id 			TEXT	NOT NULL	PRIMARY KEY,
		married		DATE	NOT NULL,
		divorced 	DATE,
		husbID 		TEXT	NOT NULL,
		wifeID 		TEXT	NOT NULL,

		FOREIGN KEY (husbID) REFERENCES individuals(id)
		FOREIGN KEY (wifeID) REFERENCES individuals(id)
	)''')

	curs.execute('''CREATE TABLE children (
		indID		TEXT	NOT NULL,
		famID		TEXT	NOT NULL,

		PRIMARY KEY (indID, famID),

		FOREIGN KEY (indID) REFERENCES individuals(id),
		FOREIGN KEY (famID) REFERENCES families(id)
	)''')

	conn.commit()

	return conn

def addIndividual (idStr, firstName, lastName, gender, birth, death):
<<<<<<< Updated upstream
	
	result = True
	
	try:
		conn.cursor().execute(
			'INSERT INTO individuals VALUES (?, ?, ?, ?, ?, ?)',
			(idStr, firstName, lastName, gender, birth, death)
		)
	
	except sqlite3.IntegrityError as err:
		print("Couldn't add individual " + idStr + ": " + str(err))
		result = False 
	
=======

	conn.cursor().execute(
		'INSERT INTO individuals VALUES (?, ?, ?, ?, ?, ?)',
		(idStr, firstName, lastName, gender, birth, death)
	)

>>>>>>> Stashed changes
	conn.commit()
	
	return result



def addFamily (idStr, married, divorced, husbID, wifeID):
<<<<<<< Updated upstream
	
	result = True
	
	try:
		conn.cursor().execute(
			'INSERT INTO families VALUES (?, ?, ?, ?, ?)',
			(idStr, married, divorced, husbID, wifeID)
		)
	
	except sqlite3.IntegrityError as err:
		print("Couldn't add family " + idStr + ": " + str(err))
		result = False 
	
=======

	conn.cursor().execute(
		'INSERT INTO families VALUES (?, ?, ?, ?, ?)',
		(idStr, married, divorced, husbID, wifeID)
	)

>>>>>>> Stashed changes
	conn.commit()
	
	return result



def addChild (childID, famID):
<<<<<<< Updated upstream
	
	result = True
	
	try:
		conn.cursor().execute(
			'INSERT INTO children VALUES (?, ?)',
			(childID, famID)
		)
	
	except sqlite3.IntegrityError as err:
		print("Couldn't add child " + childID + ": " + str(err))
		result = False 
	
=======

	conn.cursor().execute(
		'INSERT INTO children VALUES (?, ?)',
		(childID, famID)
	)

>>>>>>> Stashed changes
	conn.commit()
	
	return result



def getIndividuals():

	return conn.cursor().execute('SELECT * FROM INDIVIDUALS ORDER BY id').fetchall()



def getIndividual(indID):

	return conn.cursor().execute(
		'SELECT * FROM INDIVIDUALS WHERE id=?',
		(indID,)
	).fetchone()



def getFamilies():

	return conn.cursor().execute('SELECT * FROM FAMILIES ORDER BY id').fetchall()



def getFamily(famID):

	return conn.cursor().execute(
		'SELECT * FROM FAMILIES WHERE id=?',
		(famID,)
	).fetchall()



conn = dbInit()

addIndividual("I1", "Bob", "Dyalan", "M", "5-24-1941", None)
addIndividual("I2", "Hillary", "Clinton", "F", "10-26-1947", None)
addIndividual("I3", "Miranda", "Cosgrove", "F", "5-14-1993", None)
addFamily("F1", "6-15-1972", None, "I1", "I2")
addChild("I3", "F1")

print(getIndividuals())

conn.close()
