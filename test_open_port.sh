# use nc to test if a port is open
# Usage: test_open_port.sh <host> <port>
host=$1
port=$2
timeout=1
echo "Testing $host port $port"
nc -z -w $timeout $host $port
if [ $? -eq 0 ]; then
    echo "Port $port is open on $host"
else
    echo "Port $port is closed on $host"
fi

