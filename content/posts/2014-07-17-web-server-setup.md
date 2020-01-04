---
slug: web-server-setup
date: "2014-07-17T00:00:00Z"
description: Web Server Setup on my Mac
tags:
- web server
- setup
- mac
title: Web Server Setup on my Mac
---
I used MacPorts to handle all of these installations. I guess I should have tried php54 or even php55, but I was partially following instructions [here](http://dsheiko.com/weblog/my-lovely-mac-os-x-web-development-environment) and wanted to just get something working first.

Here's a list of commands

    sudo port -v selfupdate
    sudo port upgrade outdated
    sudo port install apache2
    sudo port install php56 +apache2
    sudo port install php56-mysql
    sudo port install mysql56-server
    sudo port install phpmyadmin +php56

	sudo port select mysql mysql56

Setting up mysql

	sudo /opt/local/lib/mysql56/bin/mysql_install_db --user mysql
    sudo chown -R mysql:mysql /opt/local/var/db/mysql56/ 
    sudo chown -R mysql:mysql /opt/local/var/run/mysql56/ 
    sudo chown -R mysql:mysql /opt/local/var/log/mysql56/
	mysqladmin -u root -p password <new-password> 

Setting up PHP to work with apache

    sudo port install php56-apache2handler
    cd /opt/local/apache2/modules
    sudo /opt/local/apache2/bin/apxs -a -e -n php5 mod_php56.so

Update Apache’s httpd.conf file. Search for and modify

    DirectoryIndex index.php index.html

Add these lines to httpd.conf too

    # For PHP
    Include conf/extra/mod_php56.conf

	# For phpMyAdmin
	Include conf/extra/httpd-phpmyadmin.conf

Create /opt/local/apache2/conf/extra/httpd-phpmyadmin.conf and add the following as contents

    AliasMatch ^/phpmyadmin(?:/)?(/.*)?$ "/opt/local/www/phpmyadmin$1"
    
    <Directory "/opt/local/www/phpmyadmin">
        Options -Indexes
        AllowOverride None
        Order allow,deny
        Allow from all
        LanguagePriority en de es fr ja ko pt-br ru 
        ForceLanguagePriority Prefer Fallback
    </Directory>

Edit phpMyAdmin config file: /opt/local/www/phpmyadmin/config.inc.php

    $cfg['Servers'][$i]['auth_type'] = 'config';
    $cfg['Servers'][$i]['user'] = 'root';
    $cfg['Servers'][$i]['password'] = '<new-password>';

Edit this line to AllowNoPassword.

    $cfg['Servers'][$i]['AllowNoPassword'] = true;

PHP config files

	cd /opt/local/etc/php5
    sudo cp php.ini-development php.ini

Follow instructions from MacPorts

    To use mysqlnd with a local MySQL server, edit /opt/local/etc/php5/php.ini and set mysql.default_socket,
    mysqli.default_socket and pdo_mysql.default_socket to the path to your MySQL server's socket file.
    
    For mysql5, use /opt/local/var/run/mysql5/mysqld.sock
    For mysql51, use /opt/local/var/run/mysql51/mysqld.sock
    For mysql55, use /opt/local/var/run/mysql55/mysqld.sock
    For mysql56, use /opt/local/var/run/mysql56/mysqld.sock
    For mariadb, use /opt/local/var/run/mariadb/mysqld.sock
    For percona, use /opt/local/var/run/percona/mysqld.sock

To prevent auto-starting of the daemons on boot, I did

    sudo launchctl unload /Library/LaunchDaemons/org.macports.apache2.plist
	sudo launchctl unload /Library/LaunchDaemons/org.macports.mysql56-server.plist

But I believe you could use this too

    sudo port unload apache2
	sudo port unload mysql-server

Setting up aliases in ~/.bash_profile

    alias apachestart="sudo /opt/local/apache2/bin/apachectl -k start"
    alias apachestop="sudo /opt/local/apache2/bin/apachectl -k stop"
    alias apacherestart="sudo /opt/local/apache2/bin/apachectl -k restart"
    alias mysqlstart="sudo /opt/local/lib/mysql56/bin/mysqld_safe &"
    alias mysqlstop="mysqladmin -u root -p shutdown"
