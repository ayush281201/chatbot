import mysql.connector

class Main:
    def __init__(self):
        self.mydb=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="ils_db")
        self.mycursor = self.mydb.cursor()

    def dealername(self, dealer_id):
        self.mycursor.execute(f"select name from tbldealers where dealer_id={dealer_id}")
        myresult = self.mycursor.fetchone()
        for x in myresult:
            dealername=x
        return dealername

    def catalogname(self, catalog_id):
        qry = f"select secure_link_title from tblinvseclinks where uuid={catalog_id}"
        self.mycursor.execute(qry)
        myresult2 = self.mycursor.fetchone()
        for x in myresult2:
            catalogtitle=x
        return catalogtitle
    def catalogname_all(self, dealerid):
        catalog = []
        qry = f"select secure_link_title from tblinvseclinks where dealer_id={dealerid}"
        self.mycursor.execute(qry)
        myresult2 = self.mycursor.fetchall()
        for x in myresult2:
            catalog.append(x[0])
        return catalog
    
    def catalogname_with_dealer(self, catalog_id, dealerid):
        qry = f"select secure_link_title from tblinvseclinks where uuid={catalog_id} and dealer_id = {dealerid}"
        self.mycursor.execute(qry)
        myresult2 = self.mycursor.fetchone()
        for x in myresult2:
            catalogtitle=x
        return catalogtitle
    
    def catalogID(self, catalogname, dealerid):
        qry = f"select uuid from tblinvseclinks where secure_link_title={catalogname} and dealer_id={dealerid}"
        self.mycursor.execute(qry)
        myresult2 = self.mycursor.fetchone()
        for x in myresult2:
            catalogtitle=x
        return catalogtitle
    
    def category(self, categoryid, dealerid):
        qry = f"select name from tblcategories where category_id={categoryid} and dealer_id={dealerid}"
        self.mycursor.execute(qry)
        myresult2 = self.mycursor.fetchone()
        for x in myresult2:
            categoryTitle=x
        return categoryTitle
