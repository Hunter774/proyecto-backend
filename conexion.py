import mysql.connector
import os


class ConexionDB:

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.conexion = None

    def conectar(self):

        if self.conexion is None or not self.conexion.is_connected():

            cert_path = os.path.join(
                os.path.dirname(__file__),
                "certs",
                "DigiCertGlobalRootCA.crt.pem"
            )

            self.conexion = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=3306,
                database=self.db,
                ssl_ca=cert_path,
                ssl_disabled=False
            )

        return self.conexion

    def obtener_cursor(self):
        return self.conectar().cursor(dictionary=True)