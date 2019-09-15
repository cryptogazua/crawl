#!/bin/bash
mkdir -p $HOME/apps
cd $HOME/apps
wget http://mirror.navercorp.com/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar xvfz spark-2.4.4-bin-hadoop2.7.tgz

rm -rf spark
ln -s spark-2.4.4-bin-hadoop2.7 spark

rm -rf $HOME/apps/spark-2.4.4-bin-hadoop2.7.tgz

if [[ -z "${SPARK_HOME}" ]]; then
    echo "export SPARK_HOME=$HOME/apps/spark" >> ~/.profile
    echo "export PATH=\${SPARK_HOME}/bin:\$PATH" >> ~/.profile
fi

source ~/.profile
