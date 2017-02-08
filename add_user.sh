echo "Creaing user..."
echo "username: test"
echo "password: test"
curl -H "Content-Type: application/json" -X POST -d '{"username":"test","password":"test"}' http://0.0.0.0:5000/api/users

echo "Auth token..."
curl -H "Content-Type: application/json" -X POST -d '{"username":"test","password":"test"}' http://0.0.0.0:5000/api/auth
