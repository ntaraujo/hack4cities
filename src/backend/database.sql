BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "vazao" (
	"id"	INTEGER NOT NULL,
	"tempo"	INTEGER NOT NULL,
	"valor"	REAL NOT NULL,
	FOREIGN KEY("id") REFERENCES "dispositivo"("id")
);
CREATE TABLE IF NOT EXISTS "dispositivo" (
	"id"	INTEGER NOT NULL UNIQUE,
	"cordx"	INTEGER NOT NULL,
	"cordy"	INTEGER NOT NULL,
	"instalacao"	INTEGER,
	"tipo"	TEXT NOT NULL DEFAULT 'N/A',
	"idproximo"	INTEGER,
	FOREIGN KEY("idproximo") REFERENCES "dispositivo",
	PRIMARY KEY("id")
);
COMMIT;
