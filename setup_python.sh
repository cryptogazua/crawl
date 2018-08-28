sudo apt-get install libssl-dev
sudo apt-get install python3-pip
pip3 install -r requirements.txt
if [[ -z "${PYSPARK_PYTHON}" ]]; then
    echo "export PYSPARK_PYTHON=python3" >> ~/.profile
fi

