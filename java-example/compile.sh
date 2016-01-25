#!/bin/bash

export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar

hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
