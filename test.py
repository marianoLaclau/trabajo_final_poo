from gestionar_obras import *


if __name__ == "__main__":
    init() # Necesario para el funcionamiento del modulo colorama

    #Comprobar la transformacion del DF mostrando el total de registros antes y despues de realizar la limpieza
    print(Fore.MAGENTA +"\nDF original, total registros y columnas: " + Style.RESET_ALL,GestionarObra.extraer_datos().shape)
    print(Fore.MAGENTA +"DF transformado, total registros y columnas: " + Style.RESET_ALL,GestionarObra.limpiar_datos().shape)
    
    
    #Mapear el modelo ORM
    GestionarObra.mapear_orm()
    
    
    #Persisitir datos obtenidos del DF en la base de datos
    GestionarObra.cargar_datos()

    
    #Creamos dos instancias de Obra  : 
    obra_hospital = GestionarObra.nueva_obra()
    obra_plaza = GestionarObra.nueva_obra()
   
    
    #Progreso de la obra pasando por todas las etapas
    print(Fore.MAGENTA+"\n\nAvance con la obra Hospital San Martin"+ Style.RESET_ALL)
    obra_hospital.nuevo_proyecto()
    obra_hospital.iniciar_contratacion()
    obra_hospital.adjudicar_obra()
    obra_hospital.iniciar_obra()
    obra_hospital.actualizar_porcentaje_avance()
    obra_hospital.incrementar_plazo()
    obra_hospital.finalizar_obra()
    
    
    


    #Progreso de la obra pasando por todas las etapas
    print(Fore.MAGENTA+"\n\nAvance con la obra Plaza Urquiza"+ Style.RESET_ALL)
    obra_plaza.nuevo_proyecto()
    obra_plaza.iniciar_contratacion()
    obra_plaza.adjudicar_obra()
    obra_plaza.iniciar_obra()
    obra_plaza.actualizar_porcentaje_avance()
    obra_plaza.incrementar_plazo()
    obra_plaza.rescindir_obra()
    
    
    
    #Finalizamos la ejecucion con los indicadores requeridos
    GestionarObra.obtener_indicadores()
    

    
 
  

    