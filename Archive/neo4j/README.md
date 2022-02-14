1. install jdk 11(need account to download since archive)
2. go to Einvironment Variable, add New > JAVA_HOME, C:\Program File\Java\jdk-vvvv AND in path, add New > %JAVA_HOME%/bin
3. go to database path(by first running neo4j and opening folder)
4. run ```.\bin\neo4j.bat install service```
5. run ```.\bin\neo4j.bat start```
6. run ```.\bin\cypher-shell -a bolt://localhost:11005 -u neo4j -p admin```


Reference
[How to set JAVA_HOME in Windows 10](https://javatutorial.net/set-java-home-windows-10)

# Reference

[Query cheatsheet](https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887)

[Comprehensive guide to graph theory and neo4j algorithms](https://go.neo4j.com/rs/710-RRC-335/images/Neo4j_Graph_Algorithms.pdf)

