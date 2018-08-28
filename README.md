# cryptogazua

Ubuntu 16.04 LTS 진행하였습니다.

## 프로젝트 다운로드
```
~$ git clone https://github.com/cryptogazua/crawl.git
~$ cd crawl
```

## 필요 프로그램 설치

* Kafka 2.11-2.0.0 설치
```
~/crawl$ ./setup_kafka.sh
```

* Spark 2.3.1 설치
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

## Steemit API 사용예제

* steemit.ipynb
* steemit.py
```
$ python3 steemit.py
```

## gazua.ini 설정파일 세팅
~/crawl$ vi gazua.ini
```
url=jdbc:mariadb://<DB IP>:3306/<DB>
user=<DB사용자>
pwd=<DB비밀번호>
```

## Steemit 처리기 실행

1. publish   프로그램 실행
```
~/crawl$ pub.sh 
```
2. subscribe 프로그램 실행
```
~/crawl$ sub.sh 
```

## 암호화폐 시세 처리기 실행

1. publish   프로그램 실행
```
~/crawl$ exchpub.sh 
```
2. subscribe 프로그램 실행
```
~/crawl$ exchsub.sh 
```
