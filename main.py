import xlrd
import mysql.connector
import datetime

book = xlrd.open_workbook("Base_2019.xls")
sheet = book.sheet_by_name("Sheet1")

database = mysql.connector.connect(host="localhost", user = "root", passwd = "senhamysql@M", db = "boticario")


cursor = database.cursor()

query = """INSERT INTO data (ID_MARCA, MARCA, ID_LINHA, LINHA, DATA_VENDA, QTD_VENDA) VALUES (%s, %s, %s, %s, %s, %s)"""

for r in range(1, sheet.nrows):
		id_marca	= sheet.cell(r,0).value
		marca	    = sheet.cell(r,1).value
		id_linha	= sheet.cell(r,2).value
		linha		= sheet.cell(r,3).value
		data_venda	= sheet.cell(r,4).value
		datetime_date = xlrd.xldate_as_datetime(data_venda, 0)
		date_object = datetime_date.date()
		data_venda = date_object.isoformat()
		qtd_venda	= sheet.cell(r,5).value

		# Assign values from each row
		values = (id_marca, marca, id_linha, linha, data_venda, qtd_venda)

		# Execute sql Query
		cursor.execute(query, values)

cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

'''
CREATE VIEW boticario.CONSOLIDADO_MARCA_ANO_MES AS
SELECT MARCA, MONTH(DATA_VENDA), YEAR(DATA_VENDA), SUM(QTD_VENDA)
from boticario.data
GROUP BY MARCA, MONTH(DATA_VENDA), YEAR(DATA_VENDA)
'''
