Ce projet se concentre sur la mise en œuvre de mécanismes d'authentification sécurisée en utilisant OpenLDAP, SSH, Apache et OpenVPN, ainsi que sur la gestion des services réseau avec DNS. De plus, il explore l'intégration de Kerberos pour une authentification renforcée.

# Partie 1 : Authentification avec OpenLDAP, SSH, Apache, OpenVPN
## Sec­tion 1 : Con­fig­ura­tion d'OpenLDAP
### 1.1 Con­fig­urez un serveur OpenLDAP avec au moins deux utilisateurs et deux groupes.

#### Étape 1: Installation du Serveur LDAP
Installez le serveur LDAP sur votre machine en utilisant la commande suivante :
```
sudo apt-get install slapd ldap-utils
```
<img width="1110" alt="Screenshot 2023-12-17 at 11 09 52 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/98825770/0b97cf98-4f09-4686-b62b-b0772cf2a604">

#### Étape 2: Configuration du Serveur LDAP
Lancez la configuration du serveur LDAP et configurez votre nom de domaine:
```
sudo dpkg-reconfigure slapd
```
![Capture d'écran 2024-01-17 085335](https://github.com/EllouzeKarim/Project-Security/assets/98825770/8c880564-1bd0-45bb-b988-29e9402c57c2)

#### Étape 3: Ajout des Groupes et des utilisateurs
Créez le fichier add_content.ldif
```
dn: ou=Groups,dc=insat,dc=tn
objectClass: organizationalUnit
ou: Groups

dn: cn=group1,ou=groups,dc=insat,dc=tn
objectClass: posixGroup
cn: group1
gidNumber: 5000

dn: cn=group2,ou=groups,dc=insat,dc=tn
objectClass: posixGroup
cn: group2
gidNumber: 5001


dn: ou=People,dc=insat,dc=tn
objectClass: organizationalUnit
ou: People

dn: uid=user1,ou=people,dc=insat,dc=tn
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: user1
sn: user1
givenName: user1
cn: user1
displayName: user1
uidNumber: 10000
gidNumber: 5000
userPassword: {SSHA}29H8YPcZ/j496fiknPwhzelFa7LB9dqw
loginShell: /bin/bash
homeDirectory: /home/ubuntu1/user1


dn: uid=user2,ou=people,dc=insat,dc=tn
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: user2
sn: user2
givenName: user2
cn: user2
displayName: user2
uidNumber: 10001
gidNumber: 5001
userPassword: {SSHA}9Rh6WT9mz/uthckTqAC+SRnIJUIwNpt0
loginShell: /bin/bash
homeDirectory: /home/ubuntu1/user2
```
#### Étape 4: Les ajouter
Exécuter votre fichier LDIF en utilisant la commande suivante :
```
ldapadd -x -D cn=admin,dc=insat,dc=tn -W -f add_content.ldif
```


### 1.2 Ajoutez des informations de votre choix y compris le certificat x509 pour tous les utilisateurs.
#### Étape 1: Ajout d'Informations Supplémentaires
Créez le fichier LDIF pour les informations supplémentaires
```
   dn: uid=user1,ou=people,dc=insat,dc=tn
   changetype: modify
   add: mail
   mail: user1@insat.tn
   -
   add: telephoneNumber
   telephoneNumber: +123456789

   dn: uid=user2,ou=people,dc=insat,dc=tn
   changetype: modify
   add: mail
   mail: user2@insat.tn
```
Exécuter ce fichier avec cette commande :
```
ldapmodify -x -D cn=admin,dc=insat,dc=tn -W -f additional-info.ldif
```
#### Étape 2: Créer les certificats
Créez un répertoire pour l'autorité de certification :
```
mkdir ~/auth
```
Générez le certificat de l'autorité de certification (CA) :
```
openssl genrsa -out ca.priv 2048
openssl rsa -in ca.priv -pubout -out ca.pub
openssl req -x509 -new -days 3650 -key ca.priv -out ca.cert
```
Générez le certificat des utilisateurs et les signer :
```
cd ~/user1
openssl genrsa -out user1.priv 2048
openssl rsa -in user1.priv -pubout -out user1.pub
openssl req -new -key user1.priv -out user1.csr

cd ~/user2
openssl genrsa -out user2.priv 2048
openssl rsa -in user2.priv -pubout -out user2.pub
openssl req -new -key user2.priv -out user2.csr

cd ~/auth
openssl x509 -req -in ~/user1/user1.csr -CA ca.cert -CAkey ca.priv -CAcreateserial -out ~/user1/user1.cert -days 3650
openssl x509 -req -in ~/user2/user2.csr -CA ca.cert -CAkey ca.priv -CAcreateserial -out ~/user2/user2.cert -days 3650
```
#### Étape 3: Ajouter ces certificats
Installez LDAP Account Manager (LAM) 
```
sudo apt -y install ldap-account-manager
```
Accédez à l'interface de gestion de LAM dans votre navigateur http://localhost/lam

Ajoutez les certificats générés aux utlisateurs

### 1.3 Assurez-vous que les utilisateurs peuvent s'authentifier avec succès sur le serveur OpenLDAP.
#### Étape 1: Configuration de la Machine Cliente
Installez les paquets LDAP client nécessaires sur la machine cliente et configuration de l'addresse IP du serveur:
```
sudo apt-get install ldap-utils libpam-ldap libnss-ldap
```
#### Étape 2: Configuration de /etc/nsswitch.conf
Éditez le fichier /etc/nsswitch.conf pour inclure LDAP dans les sources de données pour la résolution des noms :
```
sudo nano /etc/nsswitch.conf
```
Assurez-vous que les lignes suivantes incluent "ldap" :
```
passwd:         compat ldap
group:          compat ldap
shadow:         compat ldap
```
#### Étape 3: Configuration de /etc/pam.d/common-session
Éditez le fichier /etc/pam.d/common-session pour inclure la session LDAP :
```
sudo nano /etc/pam.d/common-session
```
Ajoutez la ligne suivante :
```
session required pam_mkhomedir.so skel=/etc/skel/ umask=077
```
#### Étape 3: Redémarrage des services
```
sudo systemctl restart nscd
sudo systemctl restart nslcd
```
#### Étape 3: S'assurer que les utilisateurs peuvent s'authentifier avec succès sur le serveur OpenLDAP
```
sudo login
#Donner le uid
#Donner le password
```

### 1.4 Testez la partie sécurisée de LDAP avec LDAPS et décrivez les différents avantages.
#### Étape 1: Génération d'un Certificat SSL Auto-signé
Générez un certificat auto-signé avec OpenSSL :
```
mkdir ~/ssl-ldap
openssl genrsa -aes128 -out server.key 4096
openssl rsa -in server.key  -out server.key
openssl req -new -days 3650 -key server.key -out server.csr
sudo openssl x509 -in server.csr -out server.crt -req -signkey server/key -days 3650
```
Copier le certificat et la clé dans /etc/ldap/sasl2
```
sudo cp server.key  /etc/ldap/sasl2
sudo cp server.crt  /etc/ldap/sasl2
sudo cp /etc/ssl/certs/ca-certificates.crt /etc/ldap/sasl2
sudo chown -R openldap:openldap /etc/ldap/sasl2
```
#### Étape 2: Modification des fichiers de configuration 
Créez un fichier de configuration
```
nano SSL-LDAP.ldif
```
```
dn: cn=config
changetype: modify
olcTLSCACertificateFile : /etc/ldap/sasl2/ca-certificates.crt
-
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ldap/sasl2/server.crt
-
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ldap/sasl2/server.key
```
Exécuter le fichier de configuration
```
sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f SSL-LDAP.ldif
```
Modifier /etc/default/slapd 
```
sudo nano /etc/default/slapd
```
changer SLAPD_SERVICES en :
```
SLAPD_SERVICES="ldap:/// ldapi:/// ldaps:///"
```
Modifier /etc/ldap/lapd.conf en ajoutant les deux lignes suivantes :
```
TLS_CACERT /etc/ldap/sasl2/ca-certificates.crt
TLS REQCERT allow
```
#### Étape 3: Redémarrage des services
```
sudo systemctl restart slapd
```
#### Étape 4: Vérification
```
ldapsearch -x -H ldaps://@ipserveur -b "dc=insat,dc=tn"
```
Vérifiez le port
```
netstat -antup | grep -i 636
```

## Sec­tion 2 : Authen­ti­ca­tion SSH 
### 2.1 Acti­vez l'authen­ti­ca­tion SSH via OpenLDAP.
### 2.2 Restreignez l'accès SSH aux utilisateurs du groupe approprié dans OpenLDAP.
### 2.3 Testez pour un utilisateur autorisé et un utilisateur non autorisé à SSH.

## Sec­tion 3 : Intégra­tion d'Apache 
### 3.1 Con­fig­urez Apache pour utiliser l'authen­ti­ca­tion OpenLDAP.
Installer les dépendances 
```
sudo-get install libapache2-mod-ldap-userdir libapache2-mod-authnz-external libapache2-mod-authz-unixgorup
```
### 3.2 Assurez-vous que l'accès aux pages web est limité aux membres du groupe approprié dans OpenLDAP.
#### Étape 1: Créer un fichier de configuration 
```
sudo nano /etc/apache2/sites-available/auth-ldap.conf
```
Il contiendra :
```
<Directory /var/www/html/auth-ldap>
        AuthName "ldap auth"
        AuthType Basic
        AuthBasicProvider ldap
        AuthLDAPURL ldap://localhost/dc=example,dc=com?uid?sub?(objectCLass=*)
        AuthLDAPGroupAttribute memberUid
        AuthLDAPGroupAttributeIsDN off
        AuthLDAPBindDN "cn=admin,dc=example,dc=com"
        AuthLDAPBindPassword "azerty"
        Require ldap-filter  (memberOf=cn=groupe1,ou=groups,dc=example,dc=com)
        Require ldap-group cn=groupe1,ou=groups,dc=example,dc=com
</Directory>
```
#### Étape 2: Créer le html de la page web
```
sudo mkdir /var/www/html/auth-ldap
sudo nano /var/www/html/auth-ldap/index.html
```
```
<html>
<body>
<div style ="width:100%; font-size: 40px; fonx-weight: bold; text-align: center;">
Test Page For LDAP Auth
</div>
</body>
</html>
```
#### Étape 3: Redémarrage des services et activation du site
```
a2ensite auth-ldap
systemctl restart apache2
```
### 3.3 Testez pour un utilisateur autorisé et un utilisateur non autorisé à un site web de votre choix.
Se connecter sur localhost/auth-ldap
![p1s3q3_1](https://github.com/EllouzeKarim/Project-Security/assets/98825770/ef7de0ba-15ed-4908-85ab-3465d8c73064)

![p1s3q3_2](https://github.com/EllouzeKarim/Project-Security/assets/98825770/608b5592-7403-4696-8bb2-43f3838c0b53)

![p1s3q3_3](https://github.com/EllouzeKarim/Project-Security/assets/98825770/609c1f5e-5632-4f10-9d5c-289f11ac6fa3)

![p1s3q3_4](https://github.com/EllouzeKarim/Project-Security/assets/98825770/912a3bcc-5d40-4690-90d5-2aa5efa69915)

![p1s3q3_5](https://github.com/EllouzeKarim/Project-Security/assets/98825770/421e5a11-c068-4acd-abb5-ba9714447852)



## Sec­tion 4 : Mise en place d'OpenVPN 
### 4.1 Installez et con­fig­urez OpenVPN pour utiliser l'authen­ti­ca­tion OpenLDAP.
### 4.2 Testez la connexion VPN avec succès en utilisant les informations d'OpenLDAP.
### 4.3 Testez pour un client autorisé et un client non autorisé à lancer un tunnel VPN.

# Par­tie 2 : Gestion des Services Réseau avec DNS 
## Sec­tion 1 : Con­fig­ura­tion d'un serveur DNS (20 points)
### 1.1 Con­fig­urez un serveur DNS (Bind) sur une machine distincte.
### 1.2 Ajoutez les enregistrements DNS nécessaires pour les serveurs OpenLDAP, Apache, et OpenVPN.

## Sec­tion 2 : Validation et Test 
### 2.1 Testez la résolution DNS pour chacun des services configurés.
### 2.2 Assurez-vous que les noms de domaine associés aux services sont correctement résolus.

# Par­tie 3 : Authen­ti­ca­tion avec Kerberos 
## Sec­tion 1 : Con­fig­ura­tion du serveur Kerberos
### 1.1 Installez et configurez un serveur Kerberos.

On va ajouter les DNS pour kdc et client dans /etc/host:
<img width="728" alt="Screenshot 2023-12-26 at 8 23 26 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/25b66d40-1efd-43b1-a69e-763dc2ba97f0">

essayons de faire ping aux hosts kdc et client:

<img width="687" alt="Screenshot 2023-12-26 at 8 34 31 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/c0acfb8b-9852-47fd-8f18-0409f091da0e">


<img width="711" alt="Screenshot 2023-12-26 at 8 34 17 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/5b0a162d-5266-4176-a121-1034691e2ca8">

**Synchronisation horaire:** Vérifiez que les deux machines utilisent le même fuseau horaire, tapez cette commande sur les deux machines
```
timedatectl
```

Ouvrez un terminal et exécutez les commandes suivantes pour installer les packages nécessaires :
```
sudo apt-get update
sudo apt-get install krb5-kdc krb5-admin-server
```


<img width="716" alt="Screenshot 2023-12-26 at 9 23 21 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/9df446c2-e345-4c67-b363-f1c6a151dcac">
<img width="721" alt="Screenshot 2023-12-26 at 9 26 27 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/595cd23a-6bdb-4bed-a6a2-34cc4d18365b">


 
### 1.2 Ajoutez des principaux et des poli­tiques de mot de passe pour les utilisateurs.

  Créer la base de données des principaux:

  
<img width="707" alt="Screenshot 2023-12-26 at 9 33 15 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/f47878cb-2a19-406e-b07d-f1579a765b14">


Créer les principaux:

<img width="623" alt="Screenshot 2023-12-26 at 9 40 14 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/19a44514-3119-477b-85e9-2d1cd7853a9c">
<img width="636" alt="Screenshot 2023-12-26 at 9 43 49 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/05a27112-e1d9-4fd9-8e4a-67b0816f830a">
<img width="726" alt="Screenshot 2023-12-26 at 9 51 18 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/cd3b5e4c-1510-441d-9320-62b83798ef2d">
<img width="717" alt="Screenshot 2023-12-26 at 9 54 43 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/0388a7a3-087a-4851-8946-35b33963cbf6">


Ajouter des poli­tiques de mot de passe pour les utilisateurs:

<img width="727" alt="Screenshot 2023-12-26 at 9 59 02 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/794aa293-73cb-446b-a0f8-8ef8680ed3c7">
<img width="738" alt="Screenshot 2024-01-12 at 1 15 46 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/8d744346-11e8-42a0-973a-4f42d31196e7">


## Sec­tion 2 : Authen­ti­ca­tion avec un Service Choisi 
### 2.1 Choisissez l'un des services pour implémenter l'authen­ti­ca­tion avec Kerberos.
On a choisi d'implémenter un service api avec FLASK.
nous ajouterons un principal pour utilisateur, le client qui utilisera l'application et nous lui donnerons un mot de passe:


<img width="653" alt="Screenshot 2024-01-13 at 4 34 48 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/a19cc287-5673-4f0c-8c2f-804271977e78">

Ajoutez cet utilisateur Unix correspondant à l'utilisateur principal:

<img width="621" alt="Screenshot 2024-01-13 at 4 56 26 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/d7a8ea3e-34d0-42cd-aab7-595b5f980c47">

<img width="485" alt="Screenshot 2024-01-13 at 4 57 08 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/f3fa3534-a1ae-4537-b3e8-0d28431e7f02">

Installation des package nécessaires:

<img width="732" alt="Screenshot 2024-01-13 at 11 12 06 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/20120f6e-8013-48b8-b6f8-a163e597794c">
<img width="731" alt="Screenshot 2024-01-13 at 11 12 34 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/ca719b61-4e2e-426d-8a61-e096c38479ad">

### 2.2 Documentez et configurez le service choisi pour utiliser l'authen­ti­ca­tion Kerberos.

#### Server Configuration
Nous devons définir la variable KRB5_KTNAME pour référencer le fichier keytab qui contient la clé du service:
```
export KRB5_KTNAME=/etc/krb5.keytab
```
Exécutez ensuite le fichier server.py pour lancer le serveur Flask:
```
chmod +x server/server.py
```
<img width="907" alt="Screenshot 2024-01-18 at 12 56 26 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/5343dd08-3d00-4c19-be40-02b12a4e9768">

#### Client Configuration
Ensuite, vous devrez obtenir le TGT (Ticket Granting Ticket) pour pouvoir vous authentifier plus tard sans utiliser de mot de passe, vous n'entrerez le mot de passe qu'une seule fois pour obtenir le TGT.


<img width="674" alt="Screenshot 2024-01-18 at 12 57 16 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/985f4257-52fa-4cea-83f9-c953d1e6caad">

Vous pouvez maintenant exécuter le programme et commencer à interagir:

```
chmod +x client/client.py
```
<img width="699" alt="Screenshot 2024-01-18 at 12 58 56 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/a592113c-ee44-4b44-83d2-5399f254817f">

On observe le nouveau TGT crée:


<img width="351" alt="Screenshot 2024-01-18 at 12 59 07 AM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/e11f52f3-af5d-4bf6-b7da-e8e9d2447723">

