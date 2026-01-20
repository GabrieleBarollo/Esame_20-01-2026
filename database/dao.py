from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def read_specific_artist(m):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT art.id, art.name
                FROM artist art, album al
                WHERE art.id = al.artist_id
                GROUP BY art.id, art.name
                HAVING COUNT(*) >= %s
                """
        cursor.execute(query, (m,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_edges(m):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select alb.artist_id, t.genre_id, g.name
                from album alb, track t, genre g
                where t.album_id = alb.id and g.id = t.genre_id and alb.artist_id in ( SELECT art.id
                                                                                        FROM artist art, album al
                                                                                        WHERE art.id = al.artist_id
                                                                                        GROUP BY art.id, art.name
                                                                                        HAVING COUNT(*) >= %s)
                        
                """
        cursor.execute(query, (m,))
        for row in cursor:
            result.append([row["artist_id"], row["genre_id"]])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def q(durata_ms, m):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT distinct(al.artist_id)
                    FROM album al, track t
                    WHERE t.album_id = al.id and t.milliseconds >= %s and al.artist_id in ( SELECT art.id
                                                                                                    FROM artist art, album al
                                                                                                    WHERE art.id = al.artist_id
                                                                                                    GROUP BY art.id, art.name
                                                                                                    HAVING COUNT(*) >= %s)
        
                """
        cursor.execute(query, (durata_ms,m))
        for row in cursor:
            result.append(row["artist_id"])
        cursor.close()
        conn.close()
        return result

