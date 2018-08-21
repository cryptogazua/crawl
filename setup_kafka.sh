#!/bin/bash
mkdir -p $HOME/apps
cd $HOME/apps
wget http://mirror.navercorp.com/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz
tar xvfz kafka_2.11-2.0.0.tgz

rm -rf kafka
ln -s kafka_2.11-2.0.0 kafka

rm -rf $HOME/apps/kafka_2.11-2.0.0.tgz

if [[ -z "${KAFKA}" ]]; then
    echo "export KAFKA=$HOME/apps/kafka" >> ~/.profile
    echo "export PATH=\${KAFKA}/bin:\$PATH" >> ~/.profile
fi

source ~/.profile
