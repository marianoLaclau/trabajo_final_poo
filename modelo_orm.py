from peewee import *
from datetime import datetime
from colorama import init, Fore, Style  #Con este modulo podemos formatear las salidas por consola -> (pip install colorama)



init() # Necesario para el funcionamiento del modulo colorama


#Conexion a la base de datos
sqlite_db = SqliteDatabase('./obras_urbanas.db', pragmas={'journal_mode': 'wal'})



#Decorador para conectar a la BD
def conectar_db (function):

        def wrapper (*args,**kwargs):
            try:
                sqlite_db.connect()
                result = function(*args,**kwargs)
                sqlite_db.close()
                return result
            
            except OperationalError as e:
                return print("Se ha generado un error en la conexión a la BD. " + str(e))
        
        return wrapper   




#-----------------------------------------Diseño de modelos------------------------------------------


class BaseModel(Model):
    class Meta:
        database = sqlite_db



#----------------Tablas lookup--------------------
class EtapaObra(BaseModel):
    etapa = CharField(unique=True)
    
    def __str__(self):
        return str(self.etapa)
    
    class Meta:
        db_table = 'etapa'


class TipoObra(BaseModel):
    tipo = CharField(unique=True)
    
    def __str__(self):
        return str(self.tipo)
    
    class Meta:
        db_table = 'tipo'


class AreaResponsable(BaseModel):
    area = CharField(unique=True)
    
    def __str__(self):
        return str(self.area)
    
    class Meta:
        db_table = 'area'                


class TipoContratacion(BaseModel):
    contratacion_tipo = CharField(unique=True)
    
    def __str__(self):
        return str(self.contratacion_tipo)
    
    class Meta:
        db_table = 'contratacion_tipo'




#-----------------------------Tablas--------------------------

class Obra(BaseModel):
    entorno = CharField(max_length=50 )
    nombre = CharField(max_length=50 )
    etapa = ForeignKeyField(EtapaObra)
    tipo = ForeignKeyField(TipoObra)
    area = ForeignKeyField(AreaResponsable) 
    descripcion = CharField()
    comuna = CharField(max_length=50 ) 
    barrio = CharField(max_length=50 ) 
    direccion = CharField(max_length=50 ) 
    monto_contrato = IntegerField()
    fecha_inicio = DateTimeField()
    fecha_fin_inicial = DateTimeField()
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    financiamiento = CharField(max_length=50 )
    licitacion_oferta_empresa = CharField(max_length=50)
    licitacion_anio = DateTimeField()
    contratacion_tipo = ForeignKeyField(TipoContratacion)
    nro_contratacion = IntegerField()
    cuit_contratista = IntegerField()
    mano_obra = IntegerField()
    expediente_numero = IntegerField()
    
    
    
    def nuevo_proyecto (self):
        try:
            with sqlite_db.atomic():
                print(Fore.MAGENTA+'\nEstas iniciando un nuevo proyecto, completa los siguientes campos: \n'+ Style.RESET_ALL,)

                #ForeignKey
                print("Tipos de obra: ")
                tipos = TipoObra.select()
                for tipo in tipos:
                        print(f"ID-{tipo.id} : {tipo.tipo}")
                tipo = int(input("\nIngrese el ID correspondiente al tipo de obra: "))  

                #ForeignKey
                print("\nAreas Responsables: ")
                areas = AreaResponsable.select()
                for area in areas:
                        print(f"ID-{area.id} : {area.area}")
                area = int(input("\nIngrese el ID correspondiente al area responsable de la obra: "))   
                    
                
                fecha_inicio = datetime.now()
                
                
                expediente = int(input("Ingrese el numero de expediente del nuevo proyecto(solo numeros): "))
                
                
                comuna = int(input("Ingrese el numero correspondiente a la comuna donde se realizara: "))
                barrio = input("Ingrese el barrio donde se realizara la obra: ")
                direccion = input("Ingrese la direccion de donde se realizara la obra: ")
            
                self.fecha_inicio = fecha_inicio
                self.expediente_numero = expediente
                self.area = area
                self.barrio = barrio
                self.tipo = tipo
                self.comuna=comuna
                self.direccion=direccion
                self.save()
                return print("Se ha iniciado el proyecto correctamente")
            
        except IntegrityError as e:
            return print("Error al iniciar el nuevo proyecto de obra:", e)
    

    
    
    def iniciar_contratacion (self):
        print(Fore.MAGENTA+"\nSe iniciara el proceso de contratacion"+ Style.RESET_ALL,)
        try:
            with sqlite_db.atomic():
                print("Tipos de contratación: ")
                contrataciones_tipos = TipoContratacion.select()
                for contratacion_tipo in contrataciones_tipos:
                    print(f"ID-{contratacion_tipo.id} : {contratacion_tipo.contratacion_tipo}")
                 
                contratacion_tipo_id = int(input("\nIngrese el ID correspondiente al tipo de contratación: ")) 
                self.contratacion_tipo = contratacion_tipo_id
            
                try:
                     num_contratacion = int(input("Asigne un numero de contratacion: "))
            
                except ValueError as e:
                   print("Debió ingresar un valor entero", e)
                self.nro_contratacion = num_contratacion
                print("Se ha asignado correctamente el numero de contratacion")
            
                self.save() 
            return print("Nuevo proyecto iniciado con exito")
            
        except IntegrityError as e:
            print("Error al iniciar la contratación:", e)


    
    def adjudicar_obra(self):
     try:
        with sqlite_db.atomic():
            print(Fore.MAGENTA+"\nEmpresas de licitación: "+ Style.RESET_ALL,)
            
            empresas_licitacion = Obra.select(Obra.id,Obra.licitacion_oferta_empresa).group_by(Obra.licitacion_oferta_empresa)
            for empresa in empresas_licitacion:
                print(f"ID-{empresa.id} : {empresa.licitacion_oferta_empresa}")
            
            empresa_id = int(input("\nIngrese el ID correspondiente a la empresa de licitación: "))
            cuit_empresa = input("Ingrese el cuit de la empresa contratista: ")
            anio_licitacion = datetime.now()
            plazo_meses = int(input("Ingrese el plazo estipulado en meses: "))
            monto_contrato = float(input("Ingrese el monto del contrato: "))
            
            
            try:
                empresa_seleccionada = Obra.get(Obra.id == empresa_id)
                self.licitacion_anio = anio_licitacion
                self.cuit_contratista = cuit_empresa
                self.licitacion_oferta_empresa = empresa_seleccionada.licitacion_oferta_empresa
                self.plazo_meses = plazo_meses
                self.monto_contrato = monto_contrato

                self.save()
                return print("Empresa adjudicada correctamente.")
            except Exception as e:
                return print(f"No se encontró una empresa con ID {empresa_id}."+str(e))

            
            
     except IntegrityError as e:
        print("Error al obtener empresas de licitación:", e)

    
    
    def actualizar_porcentaje_avance (self):
        print(Fore.MAGENTA+"\nActualizar porcentaje de avance"+ Style.RESET_ALL,)
        nuevo_porcentaje = float(input("ingrese el valor del porcentaje de avance: "))
        try:
            # Vemos que el porcentaje esté en un rango válido de 0 a 100
            if self.porcentaje_avance < nuevo_porcentaje and nuevo_porcentaje <= 100:
                with sqlite_db.atomic():
                    self.porcentaje_avance = nuevo_porcentaje
                    self.save()
                    print("Porcentaje de avance actualizado correctamente.")
            else:
                print("Error: El porcentaje debe estar en el rango de 0 a 100.")
        except IntegrityError as e:
            print("Error al actualizar el porcentaje de avance", e)

    
    
    def iniciar_obra(self):
        try:
            print(Fore.MAGENTA+"\nIniciando nueva obra..."+ Style.RESET_ALL,)

            # Solicitar valores al usuario
            destacada = input("¿La obra es destacada? (Sí/No): ").lower() == 'si'
            fecha_inicio = datetime.now()
            fecha_fin_inicial = input("Ingrese la fecha de finalización inicial (YYYY-MM-DD): ")
            fuente_financiamiento = input("Ingrese la fuente de financiamiento (debe ser un valor existente en la BD): ")
            mano_obra = int(input("Ingrese la cantidad de mano de obra: "))

            self.fecha_inicio = fecha_inicio
            self.fecha_fin_inicial = fecha_fin_inicial
            self.financiamiento = fuente_financiamiento
            self.mano_obra = mano_obra
            self.etapa = 'Iniciada'
            self.save()

            print("¡La obra ha sido iniciada exitosamente!")

        except IntegrityError as e:
            print("Error al iniciar la obra:", e)        

    
    
    def incrementar_plazo (self):
        print(Fore.MAGENTA+"\nIncrementar el plazo de finalizacion de obra"+ Style.RESET_ALL,)
        meses_a_incrementar = int(input("Ingrese la cantidad de meses que desa incrementar: "))
        try:
            with sqlite_db.atomic():
                    # actualizamos el plazo
                    self.plazo_meses += meses_a_incrementar
                    self.save()
                    print(f"Plazo incrementado en {meses_a_incrementar} meses.")
        except IntegrityError as e:
            print("Error al incrementar el plazo:", e)


    
    def incrementar_mano_de_obra(self):
     print(Fore.MAGENTA+"\nIncrementar numero de mano de obra"+ Style.RESET_ALL,)
     try:
        cantidad = int(input("Ingrese la cantidad de mano de obra a aumentar: "))
     except ValueError:
        print("Debe ingresar un número entero.")
        return

     try:
        with sqlite_db.atomic():
            self.mano_obra += cantidad
            self.save()
        print(f"La mano de obra se incrementó en {cantidad}.")
     except IntegrityError as e:
        print("Error al incrementar la mano de obra:", e)

    
    
    def finalizar_obra (self):
        try:
            
            with sqlite_db.atomic(): #si se produce un error no se completa (rollback)
                    # Cambio la etapa de la obra a finalizada
                    self.etapa ='Finalizada'
                    self.porcentaje_avance = 100
                    self.save()
                    return print(Fore.MAGENTA+"\nSe ha finalizado la obra con exito y se ha actualizado el porcentaje de avance en 100%"+ Style.RESET_ALL,)

            
        
        except IntegrityError as e:
            print("Error al finalizar la obra:", e)

    
    
    def rescindir_obra (self):
        try:
            
            with sqlite_db.atomic():
                    #si la obra no fue rescindida aun, cambiamos la etapa a rescindida
                    self.etapa = EtapaObra.get(EtapaObra.etapa == 'Rescindida')
                    self.save()
                    print(Fore.MAGENTA+"\nLa obra ha sido rescindida."+ Style.RESET_ALL)
            
        except IntegrityError as e:
            print("Error al rescindir la obra:", e)
    
    
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'obra'