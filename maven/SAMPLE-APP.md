## Creating a Sample APP for test OSS attributions:

> mvn archetype:generate -DgroupId=com.xpertians.sample -DartifactId=sample-app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

Add the POM
> cd maven/sample-app/
> mvn clean package

For testing:
> mvn exec:java -Dexec.mainClass="com.xpertians.sample.App"