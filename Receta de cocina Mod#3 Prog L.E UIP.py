from pymongo import MongoClient
from bson.objectid import ObjectId

def conectar_db(uri="mongodb://localhost:27017", db_name="recetas"):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        return db
    except Exception as e:
        print("Error al conectar a la base de datos: " + str(e))
        return None
    
def agregar_receta(db):
    nombre = input("Nombre: ")
    ingredientes = input("Ingredientes: ")
    pasos = input("Pasos: ")
    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }
    try:
        resultado = db.recetas.insert_one(receta)
        print("Receta agregado con el ID: " + str(resultado.inserted_id))
    except Exception as e:
        print("Error al agregar receta: " + str(e))

def actualizar_receta(db):
    ver_recetas(db)
    receta_id = input("Ingrese el ID de la receta a editar: ")
    try:
        receta = db.recetas.find_one({"_id": ObjectId(receta_id)})
        if receta:
            print("Ingrese los datos a cambiar (en blanco para no cambiar):")
            nombre = input(f"Nombre [{receta['nombre']}]: ") or receta['nombre']
            ingredientes = input(f"Ingredientes [{receta['ingredientes']}]: ") or receta['ingredientes']
            pasos = input(f"Pasos [{receta['pasos']}]: ") or receta['pasos']
            nuevos_datos = {
                "nombre": nombre,
                "ingredientes": ingredientes,
                "pasos": pasos
            }
            db.recetas.update_one({"_id": ObjectId(receta_id)}, {"$set": nuevos_datos})
            print("Se ha actualizado la rectea")
        else:
            print("No existe una receta con ese ID")
    except Exception as e:
        print("Ocurrio un Error al actualizar la receta " + str(e))

def eliminar_receta(db):
    ver_recetas(db)
    receta_id = input("Ingrese el ID de la receta a editar: ")
    try:
        resultado = db.recetas.delete_one({"_id": ObjectId(receta_id)})
        if resultado.deleted_count > 0:
            print("Se elimino la receta")
        else:
            print("receta no encontrada")
    except Exception as e:
        print("Ocurrio un Error al eliminar la receta: " + str(e))


def ver_recetas(db):
    try:
        recetas = db.recetas.find()
        print("\nLista de recetas: ")
        for receta in recetas:
            print(f"ID: {receta['_id']} | Nombre: {receta['nombre']} | Ingredientes: {receta['ingredientes']} | Pasos: {receta['pasos']}") 
        print()
    except Exception as e:
        print("Hubo un error al mostrar las recetas" + str(e))

def menu():
    print("\n Libro de Recetas")
    print("a) Agregar nueva receta")
    print("b) Actualizar receta ")
    print("c) Eliminar receta ")
    print("d) Ver recetas")
    print("e) Salir")
    

def main():
    db = conectar_db()
    if db is None:
        return
    while True:
        menu()
        opcion = input("Opcion: ")
        if opcion == "a":
            agregar_receta(db)
        elif opcion == "b":
            actualizar_receta(db)
        elif opcion == "c":
            eliminar_receta(db)
        elif opcion == "d":
            ver_recetas(db)
        elif opcion == "e":
            print("Saliendo..")
            break
        else:
            print("Opcion invalida. Intente de nuevo.")

if __name__ == "__main__":
    main()