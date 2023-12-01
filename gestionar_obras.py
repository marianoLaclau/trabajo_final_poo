import pandas as pd
from abc import ABC
from peewee import *
from modelo_orm import *




#Creacion clase abstracta
class GestionarObra(ABC):

    @classmethod
    def extraer_datos (cls):
        try:
            archivo_csv = "./observatorio-de-obras-urbanas.csv"
            df = pd.read_csv(archivo_csv, sep=",")
            return df
        
        except FileNotFoundError as e:
            return print("Error al conectar con el dataset. " + str(e) )

    
  
    
    @classmethod
    @conectar_db
    def mapear_orm (cls):
        try:
            sqlite_db.create_tables([EtapaObra, TipoObra, AreaResponsable, TipoContratacion, Obra],safe=False) #El argumento safe=False ,solo permite  crear tablas que no existen
           
            return print("Tablas creadas exitosamente.")
           
        
        except OperationalError as e:
            return print("Error al crear tablas: " + str(e))

    
    
    
    @classmethod
    def limpiar_datos (cls): 
        try:  
            df = cls.extraer_datos()
            
            #Eliminar columnas que no incluye el modelo ORM
            df.drop(['lat'], axis=1, inplace=True)
            df.drop(['lng'], axis=1, inplace=True)
            df.drop(['imagen_1'], axis=1, inplace=True)
            df.drop(['imagen_2'], axis=1, inplace=True)
            df.drop(['imagen_3'], axis=1, inplace=True)
            df.drop(['imagen_4'], axis=1, inplace=True)
            df.drop(['beneficiarios'], axis=1, inplace=True)
            df.drop(['compromiso'], axis=1, inplace=True)
            df.drop(['destacada'], axis=1, inplace=True)
            df.drop(['ba_elige'], axis=1, inplace=True)
            df.drop(['link_interno'], axis=1, inplace=True)
            df.drop(['pliego_descarga'], axis=1, inplace=True)
            df.drop(['estudio_ambiental_descarga'], axis=1, inplace=True)

            
            #Eliminar registros nulos o no accesibles de las columnas relevantes
            df.dropna(subset = ["ID"], axis = 0, inplace = True)
            df.dropna(subset = ["nombre"], axis = 0, inplace = True)
            df.dropna(subset = ["monto_contrato"], axis = 0, inplace = True)
            df.dropna(subset = ["etapa"], axis = 0, inplace = True)
            df.dropna(subset = ["area"], axis = 0, inplace = True)


            #Completar todos los registros sin datos para que no genere error de tipo NULL al persistir los datos en la BD
            df.fillna(' - ', inplace=True)

            return df
        
        except Exception as e:
            return print("Error al acceder al DF. " + str(e))

        

    @classmethod
    @conectar_db
    def cargar_datos (cls):
        df = cls.limpiar_datos()

        #Carga de tablas lookup con valores unicos
        columnas_a_cargar = ['etapa', 'tipo','area', 'contratacion_tipo']
        modelos = {
            'etapa': EtapaObra,
            'tipo': TipoObra,
            'area': AreaResponsable,
            'contratacion_tipo': TipoContratacion
        }
        
        for columna in columnas_a_cargar:
            datos_unicos = list(df[columna].unique())
            
            for elem in datos_unicos:
                try:
                    # Utiliza el nombre de la columna como atributo dinamico para la clase del modelo , los ** avisan que se pasaran 2 valores como key-value
                    modelos[columna].create(**{columna: elem })
                        
                except IntegrityError as e:
                        return print("Error al insertar un nuevo registro en la tabla etapa:" + str(e))

        
        #Carga de tabla "Obra" y "Licitacion" con los registros del DF
        for elem in df.values:

            # Las variables etapa1 , tipo1 , area1,obra1 y tipo_contrato capturan los ID de las foreign key de los registros ya existentes y los inserta en lugar de sus campos string, con el proposito de normalizar y facilitar futuros nuevos registros de obras
            etapa1 = EtapaObra.get(EtapaObra.etapa == elem[3]).id
            tipo1 = TipoObra.get(TipoObra.tipo == elem[4]).id
            area1 = AreaResponsable.get(AreaResponsable.area == elem[5]).id
            tipo_contrato = TipoContratacion.get(TipoContratacion.contratacion_tipo==elem[17]).id
            
            
            try:
                Obra.create(entorno=elem[1],nombre=elem[2],etapa=etapa1,tipo=tipo1,area=area1,descripcion=elem[6],monto_contrato=elem[7],comuna=elem[8],barrio=elem[9],direccion=elem[10],fecha_inicio=elem[11],fecha_fin_inicial=elem[12],plazo_meses=elem[13],porcentaje_avance=elem[14],financiamiento=elem[22],licitacion_oferta_empresa=elem[15],licitacion_anio=elem[16],contratacion_tipo=tipo_contrato,nro_contratacion=elem[18],cuit_contratista=elem[19],mano_obra=elem[20],expediente_numero=elem[21])
                
                
            except IntegrityError as e:
                return print("Error al insertar un nuevo registro en las tablas.", e)    
        
        
        return print("Se han persistido los datos correctamente en la BD.")

    
    
    
    @classmethod
    @conectar_db
    def nueva_obra (cls):


            print('''\nSe va a iniciar un nuevo proyecto de obra,es necesario completar los siguientes datos (Se sugiere completar todos los campos , en caso de no tener conocimiento sobre alguno se debe agregar un guion " - "): \n''')
            
            entorno = input("Ingrese el entorno donde se desarrollara la obra: ")
            nombre = input("Ingrese el nombre de la obra: ")
            
            #ForeignKey
            etapa =  EtapaObra.get(EtapaObra.etapa == 'Proyecto')

            descripcion = input("Ingrese una descripcion de la obra: ")
            
            #Los siguientes datos deberan ser cargados cuando el proyecto finalmente se inicie 
            direccion = "-"
            barrio="-"
            comuna="-"
            area="-"
            tipo="-"
            monto_contrato = "-"
            fecha_inicio = "-"
            fecha_fin_inicial = "-"
            plazo_meses = "-"
            porcentaje_avance = 0
            financiamiento = "-"   
            licitacion_oferta_empresa = "-"   
            licitacion_anio = "-"
            contratacion_tipo = "-"
            nro_contratacion = "-"
            cuit_contratista = "-"
            mano_obra = "-"
            expediente_numero = "-"

            obra_nueva = Obra(entorno=entorno,nombre=nombre,etapa=etapa,tipo=tipo,area=area,descripcion=descripcion,comuna=comuna,
                            barrio=barrio,direccion=direccion,monto_contrato=monto_contrato,fecha_inicio=fecha_inicio,fecha_fin_inicial=fecha_fin_inicial,
                            plazo_meses=plazo_meses,porcentaje_avance=porcentaje_avance,financiamiento=financiamiento,licitacion_oferta_empresa=licitacion_oferta_empresa,
                            licitacion_anio=licitacion_anio,contratacion_tipo=contratacion_tipo,nro_contratacion=nro_contratacion,cuit_contratista=cuit_contratista,mano_obra=mano_obra,
                            expediente_numero=expediente_numero)  #Se crea la nueva instancia de Obra con todos sus atributos 
        
            try:
                obra_nueva.save()
                print("Se guardaron los datos correctamente en la BD")
        
            except IntegrityError as e:
                return print("Error al cargar registros en la tabla Obra" + str(e))     
        
            return obra_nueva
    
    
    
    @classmethod
    def obtener_indicadores (cls):
        with sqlite_db.atomic():
            print(Fore.MAGENTA+"\nIndicadores de la base de datos"+Style.RESET_ALL)
            
            #Listado de todas las áreas responsables
            print("Areas responsables: ")
            for areas in AreaResponsable.select():
                print(areas)
            
            
            #Listado de todos los tipos de obra
            print("\nTipos de obra: ")
            for tipos in TipoObra.select():
                print(tipos)

            
            #Cantidad de obras que se encuentran en cada etapa
            print("\nCantidad de obras por etapa: ")
            consulta = (EtapaObra
                .select(EtapaObra.etapa, fn.COUNT(Obra.id).alias('cantidad_obras')) # Seleccionar las columnas a mostrar , con COUNT() se cuentan toda las filas que hay en Obras
                .join(Obra)
                .group_by(EtapaObra.id)) #Despues del JOIN se agrupan los datos obtenidos con la funcion COUNT()
            for etapas in consulta:
                print(f"{etapas.etapa} : {etapas.cantidad_obras} obras." )

            
            #Cantidad de obras y monto total de inversión por tipo de obra 
            print("\nCantidad de obras y monto total por tipo de obra: ")
            consulta = (TipoObra
                        .select(TipoObra.tipo,fn.COUNT(Obra.id).alias('cantidad_obras'),fn.SUM(Obra.monto_contrato).alias('monto_total')) #Seleccionar columnas a mostrar , COUNT() y SUM() muestran el total de tipos de obra y el monto total por cada tipo de obra respectivamente 
                        .join(Obra)
                        .group_by(TipoObra.id)) #Despues del JOIN se agrupan los datos obtenidos de COUNT() y SUM() segun el ID de TipoObra
            for tipos in consulta:
                print(f"{tipos.tipo} - Cantidad obras: {tipos.cantidad_obras} - Monto total por tipo: $ {tipos.monto_total}")

            
            #Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
            print("\nBarrios pertenecientes a las comunas 1,2 y 3: ")
            consulta = (Obra
                        .select(Obra.barrio)
                        .where((Obra.comuna == "1") | (Obra.comuna == "2") | (Obra.comuna == "3")) # El caracter | se usa como condicional "OR"
                        .distinct()  # Seleccionamos valores unicos , o no repetidos 
                        )
            for barrio in consulta:
                print(barrio.barrio)  #Se agrega .barrio para acceder al valor directo de la columna barrio y los imprima sin problemas al tener caracteres en mayusuclas y minusculas

            
            #Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1.
            print("\nCantidad de obras finalizadas y su monto total pertenecientes a la comuna 1: ")
            consulta = (Obra
                        .select(fn.COUNT(Obra.id).alias('cantidad_obras')
                                ,fn.SUM(Obra.monto_contrato).alias('monto_total')) #Columnas a mostrar
                        .join(EtapaObra, JOIN.INNER, on=(Obra.etapa == EtapaObra.id)) #Con JOIN.INNER solo se seleccionan las filas que tienen coincidencia en ambas tablas
                        .where((Obra.comuna == '1') & (EtapaObra.etapa == 'Finalizada')         
                        ))
            for obra in consulta:
                print(f"Cantidad de obraa finalizadas: {obra.cantidad_obras} - Monto total de inversion: $ {obra.monto_total}")

            
            #Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
            consulta =(Obra
                    .select(fn.COUNT(Obra.id).alias('cantidad_obras')) #Columna a mostrar
                    .where(Obra.plazo_meses <= 24) #Condiciona la busqueda a las que tienen un plazo menor o igual a 24
                    )
            for obra in consulta:
                print(f"\nCantidad de obras finalazadas en un plazo menor o igual a 24 meses: {obra.cantidad_obras}")

            
            #Porcentaje total de obras finalizadas
            total_obras = Obra.select(fn.COUNT(Obra.id)).scalar() #Conteo del total de obras , con .scalar() se obtienen resultados unicos usando conteos (COUNT)
            obras_finalizadas = Obra.select(fn.COUNT(Obra.id)).where(Obra.etapa == '1').scalar()  #Conteo de obras finalizadas , con .scalar() se obtienen resultados unicos usando conteos (COUNT)
            porcentaje_finalizadas = (obras_finalizadas / total_obras) * 100   #Calcular el porcentaje

            print(f"\nPorcentaje total de obras finalizadas: {round(porcentaje_finalizadas,2)} %")  #Con round(,2) se limitan los decimales despues de la coma a 2


            #Cantidad total de mano de obra empleada
            mano_obra = Obra.select(fn.SUM(Obra.mano_obra)).scalar() # Con SUM() sumamos todos los valores en mano_obra y con .scalar() guardamos el resultado unico en una variable
            print(f"\nMano de obra total empleada : {mano_obra}")


            #Monto total de inversión
            monto_total = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()
            print(f"\nMonto total invertido: $ {monto_total}")