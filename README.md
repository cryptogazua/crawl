# cryptogazua

## 내가 쓴 글이 시세에 영향을 줄까?

가상화폐거래소 시세와 Steemit 글을 Kafka를 통해 Spark Structured Streaming 처리하여 mariaDB에 저장합니다.

Ubuntu 16.04 LTS 진행하였습니다.

### Project Presentation

* [https://docs.google.com/presentation/d/19JNUkXHpQhbuaUkwi_tqa__J-cvt_aGcZENvZoO_ZIU/edit?usp=sharing](https://docs.google.com/presentation/d/19JNUkXHpQhbuaUkwi_tqa__J-cvt_aGcZENvZoO_ZIU/edit?usp=sharing)

### Dashboard

* [https://github.com/cryptogazua/gazua](https://github.com/cryptogazua/gazua)

## Docker ubuntu 16.04일 경우(option)
* docker ubuntu:16.04 실행
```
$ docker run -it ubuntu:16.04 /bin/bash
```
* git 설치
```
# apt-get update
# apt-get install git
# git clone https://github.com/cryptogazua/crawl.git
# cd crawl
```
* 최초 필요한 프로그램(패키지) 설치
```
crawl# ./setup_init.sh
```

## 프로젝트 다운로드
```
~$ git clone https://github.com/cryptogazua/crawl.git
~$ cd crawl
```

## 필요 프로그램 설치

* Kafka 2.11-2.3.0 설치
```
~/crawl$ ./setup_kafka.sh
```

* Spark 2.4.4 설치
```
~/crawl$ ./setup_spark.sh
```

* Java openjdk8 설치
```
~/crawl$ ./setup_java.sh
엔터 2번 입력
```

* Sbt 설치
```
~/crawl$ ./setup_sbt.sh
```

  * exchsub, sub 프로그램 패키지(jar) 생성
```
~/crawl$ sbt package
```

* pip3 설치 및 관련 의존성 설치
```
~/crawl$ ./setup_python.sh
엔터 2번 입력
```

* .profile 실행
```
~$ source ~/.profile
```

## Kafka 프로그램 실행

* Zookeeper 실행
```
~/crawl$ ./zoo.sh &
```

* Kafka 실행
```
~/crawl$ ./kafka.sh &
```

## Steemit API 사용예제(option)

* steemit.ipynb
* steemit.py
```
$ python3 steemit.py
```

## Database 테이블 추가

```
~/crawl$ mysql -h<DB IP> -uroot -p <DB> < gazua.sql
```

## gazua.ini 설정파일 세팅
~/crawl$ vi gazua.ini
```
url=jdbc:mariadb://<DB IP>:3306/<DB>
user=<DB사용자>
pwd=<DB비밀번호>
```

## Steemit 처리기 실행

1. publish 프로그램 실행
```
~/crawl$ nohup ./pub.sh
```
2. subscribe 프로그램 실행
```
~/crawl$ nohup ./sub.sh
```

## 암호화폐 시세 처리기 실행

1. publish   프로그램 실행
```
~/crawl$ nohup ./exchpub.sh
```
2. subscribe 프로그램 실행
```
~/crawl$ nohup ./exchsub.sh
```

## 처리기 background 실행

* 위의 4개의 sh 뒤에 인자로 nohup을 추가하면 처리기가 background 실행됩니다.
예시)
```
~/crawl$ ./exchpub.sh nohup
```
* 위의 sh을 실행하면 실제 실행되는 명령어(command)는 다음과 같습니다.
예시)
```
~/crawl$ nohup $SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 exchpub.py 2> /dev/null
```

* 참고자료 : http://sdr1982.tistory.com/215
