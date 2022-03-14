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


def gen_data():
    geninit = int(input("Tempo inicial: "))
    genend = int(input("Tempo final: "))
    devices = get_all_devices()

    for enum, d in enumerate(devices):
        if d["label"] == "Início":
            inicio = enum
            vol_vazamento = 0.1
            for time in range(geninit, genend + 1):
                data = []
                total = 0
                for d in devices:
                    randomvalue = round(random.uniform(0, 2), 1)
                    if d["label"] != "Início":
                        data.append({"id": d["id"], "tempo": time, "valor": randomvalue})
                    total += randomvalue - vol_vazamento

                data.append({"id": devices[inicio]["id"], "tempo": time, "valor": total})
                vol_vazamento += 0.05
                sql = "INSERT INTO vazao(id, tempo, valor) VALUES (?, ?, ?)"
                for entry in data:
                    db.cur.execute(sql, (entry["id"], entry["tempo"], entry["valor"]))


def gen_disps():
    num_casas = int(input("Numero de casas: "))
    cords = []

    ini_x1, ini_y1 = -23.735041298674197, -46.58108828495234
    ini_x2, ini_y2 = -23.734939435615058, -46.58102133227591
    varx, vary = ini_x2 - ini_x1, ini_y2 - ini_y1

    cords.append({"id": 16, "x": ini_x1, "y": ini_y1, "instalacao": random.randint(11111, 99999),
                  "tipo": "Início", "idproximo": 17})
    cords.append({"id": 17, "x": ini_x2, "y": ini_y2, "instalacao": random.randint(11111, 99999),
                  "tipo": "Casa", "idproximo": 18})
    for a in range(num_casas):
        x = cords[-1]["x"]
        y = cords[-1]["y"]
        print(num_casas, a)
        if num_casas/2 == a+1:
            tipo = "Intermediário"
        elif num_casas == a+1:
            tipo = "Fim"
        else:
            tipo = "Casa"
        cords.append({"id": a+18, "x": x+varx*2, "y": y+vary*2.6, "instalacao": random.randint(11111, 99999),
                      "tipo": tipo, "idproximo": a+19})

    sql = "INSERT INTO dispositivo(id, cordx, cordy, instalacao, tipo, idproximo) VALUES (?, ?, ?, ?, ?, ?)"
    for inst in cords:
        db.cur.execute(sql, (inst["id"], inst["x"], inst["y"],
                             inst["instalacao"], inst["tipo"], inst["idproximo"]))