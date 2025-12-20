
import subprocess



username = "tata"

try:
    subprocess.run(

        [ 
         "useradd", 
         "-r", 
         "-M",
         "-s", 
         "/usr/sbin/nologin", 
         username
         ] ,

         check=True
    )
    print(f"L'utilisateur {username} a été créé avec succès.")

except subprocess.CalledProcessError as error:
     print(f"Erreur lors de la création de l'utilisateur : {error}")