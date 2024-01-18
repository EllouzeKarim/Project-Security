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
![Capture d'écran 2024-01-17 123949](https://github.com/EllouzeKarim/Project-Security/assets/98825770/6eb8f627-9a64-479c-a5b3-449f4405a8c5)

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
mkdir ~/auth && cd ~/auth 
```
Générez le certificat de l'autorité de certification (CA) :
```
openssl genrsa -out ca.priv 2048
openssl rsa -in ca.priv -pubout -out ca.pub
openssl req -x509 -new -days 3650 -key ca.priv -out ca.cert
```
Générez le certificat des utilisateurs et les signer :
```
mkdir ~/user1 && cd ~/user1
openssl genrsa -out user1.priv 2048
openssl rsa -in user1.priv -pubout -out user1.pub
openssl req -new -key user1.priv -out user1.csr

mkdir ~/user2 && cd ~/user2
openssl genrsa -out user2.priv 2048
openssl rsa -in user2.priv -pubout -out user2.pub
openssl req -new -key user2.priv -out user2.csr

cd ~/auth
openssl x509 -req -in ~/user1/user1.csr -CA ca.cert -CAkey ca.priv -CAcreateserial -out ~/user1/user1.cert -days 3650
openssl x509 -req -in ~/user2/user2.csr -CA ca.cert -CAkey ca.priv -CAcreateserial -out ~/user2/user2.cert -days 3650
```
![Capture d'écran 2024-01-17 132647](https://github.com/EllouzeKarim/Project-Security/assets/98825770/37ffb03e-9a10-41b1-af6a-850bea891885)
![Capture d'écran 2024-01-17 132735](https://github.com/EllouzeKarim/Project-Security/assets/98825770/3fdbed1b-d74c-4a51-865a-41d0b0a57f6a)


#### Étape 3: Ajouter ces certificats
Installez LDAP Account Manager (LAM) 
```
sudo apt -y install ldap-account-manager
```
Accédez à l'interface de gestion de LAM dans votre navigateur http://localhost/lam

Ajoutez les certificats générés aux utlisateurs

![Capture d'écran 2024-01-17 123735](https://github.com/EllouzeKarim/Project-Security/assets/98825770/92e9c090-06c7-4ebb-83bf-09c469117045)

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
mkdir ~/ssl-ldap && cd ~/ssl-ldap
openssl genrsa -aes128 -out server.key 4096
openssl rsa -in server.key  -out server.key
openssl req -new -days 3650 -key server.key -out server.csr
sudo openssl x509 -in server.csr -out server.crt -req -signkey server.key -days 3650
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
add: olcTLSCACertificateFile
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
Modifier /etc/ldap/lapd.conf 
```
sudo nano /etc/ldap/lapd.conf 
```
en ajoutant les deux lignes suivantes :
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
![ldapsearch](https://github.com/EllouzeKarim/Project-Security/assets/98825770/e84f814c-7bef-4aef-bf4a-f63433515a70)

Vérifiez le port
```
netstat -antup | grep -i 636
```
![image](https://github.com/EllouzeKarim/Project-Security/assets/98825770/4143a504-281e-49c3-9536-0291f894a1a8)

## Sec­tion 2 : Authen­ti­ca­tion SSH 
### 2.1 Acti­vez l'authen­ti­ca­tion SSH via OpenLDAP.
#### Étape 1: Installation des packages requis 
Installez les paquets nécessaires. Cela peut être fait avec les commandes suivantes
```
sudo apt-get install openssh-server libpam-ldap
```
#### Étape 2:  Configuration de sshd_config et de PAM 
Modifiez le fichier de configuration du serveur SSH, généralement situé dans /etc/ssh/sshd_config
```
sudo nano /etc/ssh/sshd_config
```
Assurez-vous que les options suivantes sont définies :
```
PasswordAuthentication yes
ChallengeResponseAuthentication yes
UsePAM yes
```
Modifiez le fichier de configuration PAM SSH, généralement situé dans /etc/pam.d/sshd.
```
sudo nano /etc/pam.d/sshd
```
Ajoutez la ligne suivante en haut du fichier pour activer l’authentification LDAP :
```
auth required pam_ldap.so
```
### 2.2 Restreignez l'accès SSH aux utilisateurs du groupe approprié dans OpenLDAP.
Modifiez le fichier de configuration du contrôle d’accès, généralement situé dans /etc/security/access.conf.
```
sudo nano /etc/security/access.conf
```
Ajoutez la ligne suivante pour accorder l’accès aux utilisateurs du groupe LDAP « group1 » :
```
-:ALL EXCEPT group group1:ALL
```

#### Étape 3: Redémarrage des services
```
sudo service ssh restart
```

### 2.3 Testez pour un utilisateur autorisé et un utilisateur non autorisé à SSH.
Essayez de vous connecter avec un utilisateur qui appartient au groupe LDAP « group1 » et avec un qui n'y appartient pas :
```
ssh username@your_server_ip
```
![Capture d'écran 2024-01-17 222038](https://github.com/EllouzeKarim/Project-Security/assets/98825770/68e56e07-8283-4533-ae53-b6c99dbebb37)

![Capture d'écran 2024-01-17 222402](https://github.com/EllouzeKarim/Project-Security/assets/98825770/322b3af8-a7e7-4637-93d6-6d1330f5555d)

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
Assurez-vous d'installer OpenVPN sur votre serveur Ubuntu:
```
sudo apt update
sudo apt install openvpn
```
Éditez le fichier /etc/pam.d/openvpn: 
```
auth requisite pam_unix.so
auth required pam_ldap.so
account requisite pam_unix.so
account required pam_ldap.so

```
Redémarrez les services OpenVPN et LDAP pour appliquer les changements :
```
sudo systemctl restart openvpn
sudo systemctl restart slapd
```

### 4.2 Testez la connexion VPN avec succès en utilisant les informations d'OpenLDAP.
#### Server Configuration:
<img width="728" alt="Screenshot 2024-01-18 at 6 11 38 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/561be19e-e2f7-468e-93de-5c1215e73293">

exécuter le serveur openvpn
```
sudo openvpn --config server.ovpn
```
<img width="722" alt="Screenshot 2024-01-18 at 6 16 10 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/494fbaad-c8bc-47f9-9586-a8ccfa145785">

#### Client Configuration:
<img width="735" alt="Screenshot 2024-01-18 at 6 12 09 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/a5da6fb6-4eeb-4d2e-93d1-a321e04889d3">

Utilisez un client OpenVPN pour vous connecter au serveur avec les informations d'authentification OpenLDAP:
```
sudo openvpn --config client.ovpn
```
<img width="728" alt="Screenshot 2024-01-18 at 6 15 55 PM" src="https://github.com/EllouzeKarim/Project-Security/assets/79056754/c66b9794-7b55-4d46-acd5-bf137c070f5a">

# Par­tie 2 : Gestion des Services Réseau avec DNS 
## Sec­tion 1 : Con­fig­ura­tion d'un serveur DNS 
### 1.1 Con­fig­urez un serveur DNS (Bind) sur une machine distincte.
Configuration d'un serveur DNS (Bind)
Assurez-vous que votre serveur DNS Bind est correctement installé et en cours d'exécution. Si ce n'est pas le cas, installez-le et démarrez-le :
```
sudo apt-get update
sudo apt-get install bind9
sudo systemctl start bind9
sudo systemctl enable bind9
cd /etc/bind
```
Ouvrez le fichier named.conf.options et assurez-vous que les serveurs de renvoi (forwarders) sont correctement configurés :
```
sudo nano named.conf.options
```
```
forwarders {
     192.168.56.102;
     8.8.8.8;
};
```
Ouvrez le fichier named.conf.local et ajoutez les zones pour le domaine et la zone inversée :
```
sudo nano named.conf.local 
```
```
zone "insat.tn" {
    type master;
    file "/etc/bind/db.insat.tn";
};

zone "56.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/db.reverse.tn";
};
```
### 1.2 Ajoutez les enregistrements DNS nécessaires pour les serveurs OpenLDAP, Apache, et OpenVPN.
Créer le fichier db.insat.tn à partir de db.local:
```
sudo cp db.local db.insat.tn
```
Modifier le fichier db.insat.tn :
```
sudo nano db.insat.tn 
```
```
$TTL 604800
@       IN SOA  server.insat.tn. root.insat.tn. (
                3         ; Serial
                604800    ; Refresh
                86400     ; Retry
                2419200   ; Expire
                604800    ; Minimum TTL
)

@       IN NS   server.insat.tn.
@       IN A    192.168.56.102
@       IN AAAA ::1
server  IN A    192.168.56.102
apache  IN A    192.168.56.102
```
Modifier le fichier db.reverse.tn :
```
sudo nano db.reverse.tn
```
```
$TTL 604800
@       IN SOA  server.insat.tn. root.insat.tn. (
                3         ; Serial
                604800    ; Refresh
                86400     ; Retry
                2419200   ; Expire
                604800    ; Minimum TTL
)

@       IN NS   server.insat.tn.
10     IN PTR  server.insat.tn.
```
Modifier le fichier /etc/resolv.conf :
```
sudo nano /etc/resolv.conf
```
```
nameserver 192.168.56.102
domain insat.tn
search insat.tn
```
## Sec­tion 2 : Validation et Test 
### 2.1 Testez la résolution DNS pour chacun des services configurés.
Assurez-vous que le serveur DNS est en cours d'exécution.
```
sudo systemctl restart bind9
sudo systemctl status bind9
```
Utilisez la commande nslookup pour tester la résolution DNS :
```
nslookup server.insat.tn
nslookup apache.insat.tn
```
![image](https://github.com/EllouzeKarim/Project-Security/assets/98825770/ba10c9d6-4481-4635-8c47-197f8d5a8ad5)

### 2.2 Assurez-vous que les noms de domaine associés aux services sont correctement résolus.
```
nslookup 192.168.56.102
```
![image](https://github.com/EllouzeKarim/Project-Security/assets/98825770/73fe8a68-3741-4bd8-b119-a62c737e1ce7)

![image](https://github.com/EllouzeKarim/Project-Security/assets/98825770/4ca9490a-2997-4f6f-8049-143ac894791c)


![image](https://github.com/EllouzeKarim/Project-Security/assets/98825770/c719437e-94c9-4716-bda1-629ec06c4182)


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

