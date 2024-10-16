import mysql.connector
from datetime import datetime
from tabulate import tabulate

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="cuaca"
)

def create(x):
  id = input("Masukan id : ")
  lokasi = input("Masukan lokasi : ")
  tanggal = input("Gunakan waktu sekarang / input manual ? (1/2) : ")
  
  if tanggal == "1" :
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
  elif tanggal == "2" :
    waktu = input("Masukan waktu (YYYY-MM-DD HH:mm) : ")
  else :
    waktu = "None"
    print("Data yang anda inputkan salah!, anda dapat mengubahnya kembali pada menu (Mengubah Data)")
    
  suhu = float(input("Masukan suhu (Derajat Celsius) : "))
  k = kondisi (suhu)
  cursor = x.cursor()
 
  sql = "INSERT INTO informasi (id, lokasi, waktu, suhu, kondisi) VALUES (%s, %s, %s, %s, %s)"
  val = (id, lokasi, waktu, suhu, k)
  
  cursor.execute(sql, val)
  db.commit()
  print("{} data cuaca berhasil disimpan".format(cursor.rowcount))

def read(x):
  cursor = x.cursor()
  cursor.execute("SELECT COUNT(*) FROM informasi")
  jumlah_data = cursor.fetchone()[0]
  sql = "SELECT informasi.id, lokasi, waktu, suhu, keterangan FROM informasi, tingkatan WHERE kondisi = tingkatan.id ORDER BY informasi.id"
  cursor.execute(sql)
  hasil = cursor.fetchall()
  
  if jumlah_data <= 0:
    print("Tidak ada data")
  else:
    print("=============================================================")
    print("|                      INFORMASI CUACA                      |")
    print("=============================================================")
   
    header = ["id", "lokasi", "waktu", "suhu", "kondisi"]
    info = (hasil)
    table = tabulate(info, header, tablefmt="grid")
    print(table)

def update(x):
  cursor = x.cursor()
  read(x)
  print("")
  id = input (" Pilih id : > ")
  lokasi = input("Masukan lokasi : ")
  tanggal = input("Gunakan waktu sekarang / input manual ? (1/2) : ")
  
  if tanggal == "1" :
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
  elif tanggal == "2" :
    waktu = input("Masukan waktu (YYYY-MM-DD HH:mm) : ")
  else :
    waktu = "None"
    print("Data yang anda inputkan salah!, anda dapat mengubahnya kembali pada menu (Mengubah Data)")
  
  suhu = float(input("Masukan suhu (Derajat Celsius) : "))
  k = kondisi (suhu)

  sql = "UPDATE informasi SET lokasi=%s, waktu=%s, suhu=%s, kondisi=%s WHERE id=%s"
  val = (lokasi, waktu, suhu, k, id)
  cursor.execute(sql, val)
  db.commit()
  print("{} data berhasil diubah".format(cursor.rowcount))

def delete(x):
  cursor = x.cursor()
  read(x)
  print("")
  id = input("Pilih id : > ")
  sql = "DELETE FROM informasi WHERE id=%s"
  val = (id,)
  cursor.execute(sql, val)
  db.commit()
  print("{} data berhasil dihapus".format(cursor.rowcount))

def kondisi (x) : 
  if x < 27 :
    return 1
  elif x <= 31 :
    return 2
  else :
    return 3

def menu ():
  print("================================")
  print("    DATABASE INFORMASI CUACA    ")
  print("================================")
  print("1. Mengisi Data"                 )
  print("2. Menampilkan Data"             )
  print("3. Mengubah Data"                )
  print("4. Menghapus Data"               )
  print("0. Keluar"                       )
  print("================================")
  menu = input("Pilih menu : > ")
  
  if menu == "1":
    create(db)
  elif menu == "2":
    read(db)
  elif menu == "3":
    update(db)
  elif menu == "4":
    delete(db)
  elif menu == "0":
    exit()
  else:
    print("Menu salah!, silahkan masukan ulang")

if __name__ == "__main__":
  while(True):
    menu()