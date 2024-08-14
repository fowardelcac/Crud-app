CREATE TABLE Companies (
Company_id INTEGER PRIMARY KEY AUTOINCREMENT,
Company_name TEXT NOT NULL,
Location TEXT,
Company_phone TEXT,
Company_email TEXT
);

CREATE TABLE Contacts (
Contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
Contact_name TEXT NOT NULL,
Contact_phone TEXT NOT NULL,
Contact_email TEXT,
Job_position TEXT,
Company_id INTEGER NOT NULL,
FOREIGN KEY(Company_id) REFERENCES Companies(Company_id) 
ON DELETE CASCADE
);

CREATE TABLE Constructions (
Construction_id INTEGER PRIMARY KEY AUTOINCREMENT,
Construction_name TEXT NOT NULL,
Description TEXT,
Type_of_task TEXT NOT NULL,
Direction TEXT,
Start_date TEXT,
Possible_end_date TEXT,
Budget REAL,
Total_payment REAL,
Partial_payment REAL,
Company_id INTEGER NOT NULL,
FOREIGN KEY(Company_id) REFERENCES Companies(Company_id) 
ON DELETE CASCADE
);

CREATE TABLE Items (
Item_id INTEGER PRIMARY KEY AUTOINCREMENT,
Item_name TEXT NOT NULL,
Description TEXT,
Start_date TEXT,
Possible_end_date TEXT,
Completed TEXT,
Construction_id INTEGER NOT NULL,
FOREIGN KEY(Construction_id) REFERENCES Constructions(Construction_id) ON DELETE CASCADE
);

CREATE TABLE Maintenances (
Maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
Type TEXT,
Description TEXT,
Last_maintenance TEXT,
Next_maintenance TEXT,
Item_id INTEGER NOT NULL,
FOREIGN KEY(Item_id) REFERENCES Items(Item_id) ON DELETE CASCADE
);

#Indice para mejorar la busqueda
CREATE UNIQUE INDEX idx_company ON Companies(Company_name);
CREATE INDEX idx_construction ON Constructions(Construction_name);

# Tablas de ejemplo
INSERT INTO Companies (Company_name, Location, Company_phone, Company_email)
VALUES
("Siglo 21", "ituzaingo 221 Cordoba", "351682242", "@Siglo21"),
("Siglo10", "nueva 221", "122222", "@12345"),
("BLasPAscal", "celso barrios", "351682242", "@blaspascal"),
("Empresa A", "Avenida Siempre Viva 123 Springfield", "123456789", "contacto@empresaa.com"),
("Empresa B", "CShelbyville", "987654321", "info@empresab.com"),
("Empresa C", "Boulevard de los Sueños 789", "555666777", "ventas@empresac.com"),
("Empresa D", "Ruta 66", "444555666", "servicios@empresad.com"),
("Empresa E", "Calle del Comercio 10", "333444555", "compras@empresae.com"),
("Empresa F", "Avenida Principal 15", "111222333", "administracion@empresaf.com"),
("Empresa G", "Gotham", "999888777", "soporte@empresag.com"),
("Empresa H", "Plaza Mayor 25", "888777666", "contacto@empresah.com"),
("Empresa I", "Parque Industrial 30", "777666555", "info@empresai.com"),
("Empresa J", "Puerto Libre", "666555444", "ventas@empresaj.com");

INSERT INTO Contacts (Contact_name, Contact_phone, Contact_email, Job_position, Company_id)
VALUES
("Javier Milei", "35151872", "@VLLC", "Presidente", 1),
("Solana", "1234567", "juana@loka.com", "CEO", 1),
("Dua", "77494007", "dualipa@gmail.com", "CTO", 2),
("Ana Gómez", "5551234", "ana@empresaa.com", "Gerente de Ventas", 1),
("Luis Martínez", "5555678", "luis@empresab.com", "Director de Marketing", 2),
("Carlos Pérez", "5559101", "carlos@empresac.com", "Jefe de Proyectos", 3),
("María López", "5551122", "maria@empresad.com", "Responsable de RRHH", 4),
("Fernando Ruiz", "5553344", "fernando@empresae.com", "Técnico de Soporte", 5),
("Lucía Sánchez", "5555566", "lucia@empresaf.com", "Asistente Administrativa", 6),
("David Fernández", "5557788", "david@empresag.com", "Analista Financiero", 7),
("Elena García", "5559900", "elena@empresah.com", "Consultora de IT", 8),
("José Ramírez", "5552233", "jose@empresai.com", "Ingeniero de Software", 9),
("Isabel Morales", "5554455", "isabel@empresaj.com", "Coordinadora de Logística", 10);

INSERT INTO Constructions (Construction_name, Description, Type_of_task, Direction, Start_date, 
Possible_end_date, Budget, Total_payment, Partial_payment, Company_id)
VALUES
("Edificio Central", "Construcción del edificio central de oficinas", "Construcción", "Avenida Siempre Viva 123", "01/01/2024", "31/12/2024", 1000000.00, 500000.00, 250000.00, 1),
("Planta Industrial", "Edificación de una nueva planta industrial", "Plomería", "Calle Falsa 456", "15/02/2024", "15/02/2025", 2000000.00, 1000000.00, 500000.00, 2),
("Centro Comercial", "Construcción de un centro comercial", "Electricidad", "Boulevard de los Sueños 789", "01/03/2024", "01/03/2025", 1500000.00, 750000.00, 375000.00, 3),
("Parque Empresarial", "Desarrollo de un parque empresarial", "Aires y servicios", "Ruta 66", "10/04/2024", "10/04/2025", 3000000.00, 1500000.00, 750000.00, 4),
("Torre Residencial", "Construcción de una torre de apartamentos", "Construcción", "Calle del Comercio 10", "05/05/2024", "05/05/2025", 2500000.00, 1250000.00, 625000.00, 5),
("Complejo Deportivo", "Desarrollo de un complejo deportivo", "Aires y servicios", "Avenida Principal 15", "15/06/2024", "15/06/2025", 1800000.00, 900000.00, 450000.00, 6),
("Hospital General", "Construcción de un hospital general", "Aires y servicios", "Calle Secundaria 20", "01/07/2024", "01/07/2025", 2200000.00, 1100000.00, 550000.00, 7),
("Centro de Convenciones", "Edificación de un centro de convenciones", "Aires y servicios", "Plaza Mayor 25", "10/08/2024", "10/08/2025", 2700000.00, 1350000.00, 675000.00, 8),
("Universidad", "Construcción de una universidad", "Aires y servicios", "Parque Industrial 30", "01/09/2024", "01/09/2025", 3200000.00, 1600000.00, 800000.00, 9),
("Estadio", "Desarrollo de un estadio", "Aires y servicios", "Zona Franca 35", "15/10/2024", "15/10/2025", 3500000.00, 1750000.00, 875000.00, 10);

INSERT INTO Items (Item_name, Description, Start_date, Possible_end_date, Completed, Construction_id)
VALUES
("Fundación y estructura", "Construcción de la fundación y la estructura del edificio", "05/01/2024", "05/03/2024", "No", 1),
("Instalaciones eléctricas", "Instalación del sistema eléctrico del edificio", "06/03/2024", "06/05/2024", "No", 1),
("Acabados interiores", "Pintura y acabados interiores", "07/05/2024", "07/07/2024", "No", 1),
("Montaje de maquinaria", "Instalación de maquinaria en la planta", "20/02/2024", "20/06/2024", "No", 2),
("Sistemas de seguridad", "Implementación de sistemas de seguridad industrial", "21/06/2024", "21/10/2024", "No", 2),
("Estructura del centro", "Construcción de la estructura del centro comercial", "10/03/2024", "10/06/2024", "No", 3),
("Tiendas y locales", "Construcción de tiendas y locales", "11/06/2024", "11/09/2024", "No", 3),
("Vías de acceso", "Construcción de vías de acceso al parque empresarial", "20/04/2024", "20/07/2024", "No", 4),
("Zonas verdes", "Desarrollo de zonas verdes y áreas recreativas", "21/07/2024", "21/10/2024", "No", 4),
("Fundación de la torre", "Construcción de la fundación de la torre", "10/05/2024", "10/07/2024", "No", 5),
("Apartamentos", "Construcción de apartamentos", "11/07/2024", "11/02/2025", "No", 5),
("Campos deportivos", "Construcción de campos deportivos", "20/06/2024", "20/10/2024", "No", 6),
("Gimnasio", "Construcción del gimnasio del complejo", "21/10/2024", "21/01/2025", "No", 6),
("Fundación del hospital", "Construcción de la fundación del hospital", "10/07/2024", "10/09/2024", "No", 7),
("Salas de operaciones", "Construcción y equipamiento de salas de operaciones", "11/09/2024", "11/01/2025", "No", 7),
("Salas de conferencias", "Construcción de salas de conferencias", "15/08/2024", "15/12/2024", "No", 8),
("Área de exposiciones", "Desarrollo del área de exposiciones", "16/12/2024", "16/03/2025", "No", 8),
("Aulas y laboratorios", "Construcción de aulas y laboratorios", "10/09/2024", "10/02/2025", "No", 9),
("Biblioteca", "Construcción de la biblioteca universitaria", "11/02/2025", "11/05/2025", "No", 9),
("Cancha principal", "Construcción de la cancha principal del estadio", "20/10/2024", "20/02/2025", "No", 10),
("Graderías", "Construcción de graderías", "21/02/2025", "21/06/2025", "No", 10);

INSERT INTO Maintenances (Type, Description, Last_maintenance, Next_maintenance, Item_id)
VALUES
("Correctivo", "Reparación de estructura", "01/08/2024", "01/11/2024", 1),
("Preventivo", "Inspección eléctrica", "15/07/2024", "15/01/2025", 2),
("Preventivo", "Mantenimiento de pintura", "01/09/2024", "01/03/2025", 3),
("Correctivo", "Revisión de maquinaria", "10/08/2024", "10/12/2024", 4),
("Preventivo", "Actualización de sistemas", "01/11/2024", "01/05/2025", 5),
("Correctivo", "Reparación de estructura", "15/09/2024", "15/03/2025", 6),
("Preventivo", "Limpieza y mantenimiento", "01/10/2024", "01/04/2025", 7),
("Preventivo", "Podado y mantenimiento", "15/10/2024", "15/04/2025", 8),
("Preventivo", "Inspección de cimientos", "20/09/2024", "20/03/2025", 9),
("Correctivo", "Reparación de biblioteca", "01/03/2025", "01/09/2025", 10);
