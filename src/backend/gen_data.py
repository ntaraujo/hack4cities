from database_interface import Database
import random


db = Database()


def get_all_devices():
    data = []
    db.cur.execute("SELECT id, cordx, cordy, instalacao, idproximo, tipo from dispositivo")
    disps = db.cur.fetchall()
    for d in disps:
        data.append({"id": d[0], "label": d[5], "proximo": d[4]})
    return data


geninit = int(input("Tempo inicial: "))
genend = int(input("Tempo final: "))
devices = get_all_devices()
# print(devices)

intermediarios = []
for enum, d in enumerate(devices):
    if d["label"] == "inicio":
        inicio = enum
        for time in range(geninit, genend + 1):
            data = []
            total = 0
            for d in devices:
                randomvalue = round(random.uniform(0, 2), 1)
                if d["label"] != "inicio":
                    data.append({"id": d["id"], "tempo": time, "valor": randomvalue})
                total += randomvalue
            data.append({"id": devices[inicio]["id"], "tempo": time, "valor": total})
            print(data)
            print(total)
            sql = "INSERT INTO vazao(id, tempo, valor) VALUES (?, ?, ?)"
            for entry in data:
                db.cur.execute(sql, (entry["id"], entry["tempo"], entry["valor"]))



# db.con.commit()