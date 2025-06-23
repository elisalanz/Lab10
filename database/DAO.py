from database.DB_connect import DBConnect
from model.country import Country


class DAO():

    @staticmethod
    def getAllCountries(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT c.CCode, c.StateAbb, c.StateNme
                    FROM country c, contiguity co
                    WHERE c.CCode = co.state1no AND co.year<=%s"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Country(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT state1no, state2no 
                    FROM contiguity 
                    WHERE conttype=1 AND year<=%s AND state1no<state2no"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append((idMap[row['state1no']], idMap[row['state2no']]))
        cursor.close()
        conn.close()
        return result