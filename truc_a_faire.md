1. S'occuper de la gesion des rivileges lors de la creation de la BDD
   Je pense qu'il faut exécécuter les lignes suivantes dans la bdd...remplacer
   CREATE USER 'epicevents*user'@'localhost' IDENTIFIED BY 'your_password';  
   GRANT ALL PRIVILEGES ON *.\* TO 'epicevents_user'@'localhost';
   FLUSH PRIVILEGES;

2. Architexture de l'appli

3. Test

J"tais en train de fix assign support contact...
