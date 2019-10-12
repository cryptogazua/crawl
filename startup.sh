echo "rm -rf /tmp/*"
rm -rf /tmp/*
sleep 10
echo "./zoo.sh > zoo.txt &"
./zoo.sh > zoo.txt &
sleep 10
echo "./kafka.sh > kafka.txt &"
./kafka.sh > kafka.txt &
sleep 10
echo "./pub.sh > pub.txt &"
./pub.sh > pub.txt &
sleep 10
echo "./exchpub.sh > exchpub.txt &"
./exchpub.sh > exchpub.txt &
sleep 10
echo "./sub.sh > sub.txt &"
./sub.sh > sub.txt &
sleep 10
echo "./exchsub.sh > exchsub.txt &"
./exchsub.sh > exchsub.txt &
