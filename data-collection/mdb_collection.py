import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# https://www.bundestag.de/services/opendata
# Stammdaten aller Abgeordneten seit 1949 im XML-Format (Stand 07.04.2022)
root = ET.parse('../data/external/MdB-Stammdaten-data/MDB_STAMMDATEN.XML').getroot()

i = 0

mdb_list = pd.DataFrame(columns=['bundestag_id', 'nachname', 'vorname', 'geburtsdatum', 'geburtsort', 'geburtsland', 'geschlecht', 'familienstand', 'religion', 'beruf', 'wp', 'mdbwp_von', 'mdbwp_bis', 'wkr_nummer', 'wkr_name', 'wkr_land', 'liste', 'mandatsart', 'fraktion', 'ministerium', 'fkt_lang'])

for child in root:
	# print("\n### Mitglied des Bundestags ###")
	# print(child.tag, child.text)
	if child.tag == "MDB":
		mdb_entry = []
		for elem in child:

			# Get ID
			if elem.tag == "ID":
				mdb_entry.append(elem.text)
			
			# Add name
			if elem.tag == "NAMEN":
				for namen in elem[-1]:
					if namen.tag == "NACHNAME":
						mdb_entry.append(namen.text)
					if namen.tag == "VORNAME":
						mdb_entry.append(namen.text)

			if elem.tag == "BIOGRAFISCHE_ANGABEN":
				for biografische_angaben in elem:
					if biografische_angaben.tag == "GEBURTSDATUM":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "GEBURTSORT":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "GEBURTSLAND":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "GESCHLECHT":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "FAMILIENSTAND":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "RELIGION":
						mdb_entry.append(biografische_angaben.text)
					if biografische_angaben.tag == "BERUF":
						mdb_entry.append(biografische_angaben.text)

			# Detect legislative period and only add politicans of 20th German Bundestag
			if elem.tag == "WAHLPERIODEN":
				for elem1 in elem:

					add = False
					# Wahlperiode
					for elem2 in elem1:
						
						# Detect legislative period and only add politicans of 20th German Bundestag
						if elem2.tag == "WP":#
							if elem2.text == "20":
								mdb_entry.append(elem2.text)
								add = True # set flag to true
								i += 1 # It should be 736 but one politican changed with another one

						if add == True:
							if elem2.tag == "MDBWP_VON":
								mdb_entry.append(elem2.text)
							if elem2.tag == "MDBWP_BIS":
								mdb_entry.append(elem2.text)	
							if elem2.tag == "WKR_NUMMER":
								mdb_entry.append(elem2.text)	
							if elem2.tag == "WKR_NAME":
								mdb_entry.append(elem2.text)
							if elem2.tag == "WKR_LAND":
								mdb_entry.append(elem2.text)
							if elem2.tag == "LISTE":
								mdb_entry.append(elem2.text)
							if elem2.tag == "MANDATSART":
								mdb_entry.append(elem2.text)

						if add == True:
							# print(i, add)
							if elem2.tag == "INSTITUTIONEN": 
								# print(i, add, elem2.tag)

								for institutionen in elem2:

									addFraktion = False
									addMinisterium = False
									for institution in institutionen:
										
										# first detect if the institution in the nested array is of type fraction, then add the name of the fraction to the data set
										if institution.tag == "INSART_LANG":
											if institution.text == "Fraktion/Gruppe":
												addFraktion = True

										if addFraktion == True and institution.tag == "INS_LANG":

											# if information about a fraction was already found, skip the entry
											# bug: if the person changed the party during 20th bundestag, the first party is used
											# after checking data, as of 21th May only Uwe Witt and Johannes Huber are affected by this
											if len(mdb_entry) == 18:
												mdb_entry.append(institution.text)
											addFraktion = False

										if institution.tag == "INSART_LANG":
											if institution.text == "Ministerium":
												addMinisterium = True

										if len(mdb_entry) == 19:
											mdb_entry.append(None)
											mdb_entry.append(None)

										if addMinisterium == True and institution.tag == "INS_LANG":
											print(mdb_entry[2], mdb_entry[1])
											print("INS_LANG", institution.text, len(mdb_entry))
											if len(mdb_entry) == 21:
												if mdb_entry[-2] is None:
													mdb_entry[-2] = institution.text

										if addMinisterium == True and institution.tag == "FKT_LANG":
											print("FKT_LANG", institution.text, len(mdb_entry))
											if len(mdb_entry) == 21:
												mdb_entry.pop()
												mdb_entry.append(institution.text)

									addMinisterium = False

									addFraktion = False

					# Check flag if data entry should be added to data frame
					if add == True:
						# print(mdb_entry)
						mdb_list.loc[len(mdb_list.index)] = mdb_entry	

			# TODO: Add more available information to the table

			## NAMEN ##
			# Ortszusatz
			# Adel
			# Präfix
			# Anrede_Titel
			# Akad_Titel
			# Historie_Von
			# Historie_Bis

			## Biografische Angaben ##
			# Partei_Kurz
			# Vita_Kurz
			# Veröffentlichpflichtiges

			## Wahlperiode ##

			# MDBWP_VON
			# MDBWP_BIS
			# WKR_NUMMER
			# WKR_NAME (Wahlkreis Name)
			# WKR_LAND
			# LISTE
			# MANDATSART
			# INSTITUTIONEN (nested) (zB Fraktion/Gruppe, Ministerium, Ausschuss, Sonstiges Gremium)


print("Anzahl Politiker:", i)

print(mdb_list)
file_path = '../data/intermediate/mdb_list/mdb_list.csv'
mdb_list.to_csv(file_path, index=False, decimal=',', sep=";", float_format='%.0f')
