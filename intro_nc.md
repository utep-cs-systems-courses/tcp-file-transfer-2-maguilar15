# Intro to Netcat 

# Forward Proxy

./fileClient.py -s 127.0.0.1:50000

**%>** nc www.utep.edu 80 

**%>** nc -v www.utep.edu 80 

**%>** nc -d www.utep.edu 80

# Start Server 

**%>** nc 127.0.0.1 5000 

# Start Listener 

**%>** nc -l 5000
