# Project-Security
Ce projet se concentre sur la mise en œuvre de mécanismes d'authentification sécurisée en utilisant OpenLDAP, SSH, Apache et OpenVPN, ainsi que sur la gestion des services réseau avec DNS. De plus, il explore l'intégration de Kerberos pour une authentification renforcée.

# Partie 1 : Authentification avec OpenLDAP, SSH, Apache, OpenVPN
## Sec­tion 1 : Con­fig­ura­tion d'OpenLDAP
### 1.1 Con­fig­urez un serveur OpenLDAP avec au moins deux utilisateurs et deux groupes.
```
sudo apt-get install slapd ldap-utils
sudo dpkg-reconfigure slapd
```
<img width="1110" alt="Screenshot 2023-12-17 at 11 09 52 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/98825770/0b97cf98-4f09-4686-b62b-b0772cf2a604">

### 1.2 Ajoutez des informations de votre choix y compris le certificat x509 pour tous les utilisateurs.
### 1.3 Assurez-vous que les utilisateurs peuvent s'authentifier avec succès sur le serveur OpenLDAP.
### 1.4 Testez la partie sécurisée de LDAP avec LDAPS et décrivez les différents avantages.
## Sec­tion 2 : Authen­ti­ca­tion SSH (15 points)
### 2.1 Acti­vez l'authen­ti­ca­tion SSH via OpenLDAP.
### 2.2 Restreignez l'accès SSH aux utilisateurs du groupe approprié dans OpenLDAP.
### 2.3 Testez pour un utilisateur autorisé et un utilisateur non autorisé à SSH.

## Sec­tion 3 : Intégra­tion d'Apache (15 points)
### 3.1 Con­fig­urez Apache pour utiliser l'authen­ti­ca­tion OpenLDAP.
### 3.2 Assurez-vous que l'accès aux pages web est limité aux membres du groupe approprié dans OpenLDAP.
### 3.3 Testez pour un utilisateur autorisé et un utilisateur non autorisé à un site web de votre choix.

## Sec­tion 4 : Mise en place d'OpenVPN (15 points)
### 4.1 Installez et con­fig­urez OpenVPN pour utiliser l'authen­ti­ca­tion OpenLDAP.
### 4.2 Testez la connexion VPN avec succès en utilisant les informations d'OpenLDAP.
### 4.3 Testez pour un client autorisé et un client non autorisé à lancer un tunnel VPN.

# Par­tie 2 : Gestion des Services Réseau avec DNS (40 points)
## Sec­tion 1 : Con­fig­ura­tion d'un serveur DNS (20 points)
### 1.1 Con­fig­urez un serveur DNS (Bind) sur une machine distincte.
### 1.2 Ajoutez les enregistrements DNS nécessaires pour les serveurs OpenLDAP, Apache, et OpenVPN.

## Sec­tion 2 : Validation et Test (20 points)
### 2.1 Testez la résolution DNS pour chacun des services configurés.
### 2.2 Assurez-vous que les noms de domaine associés aux services sont correctement résolus.

# Par­tie 3 : Authen­ti­ca­tion avec Kerberos (40 points)
## Sec­tion 1 : Con­fig­ura­tion du serveur Kerberos (20 points)
### 1.1 Installez et configurez un serveur Kerberos.
### 1.2 Ajoutez des principaux et des poli­tiques de mot de passe pour les utilisateurs.
  
## Sec­tion 2 : Authen­ti­ca­tion avec un Service Choisi (20 points)
### 2.1 Choisissez l'un des services (OpenLDAP, SSH, Apache, ou OpenVPN) pour implémenter l'authen­ti­ca­tion avec Kerberos.
### 2.2 Documentez et configurez le service choisi pour utiliser l'authen­ti­ca­tion Kerberos.
