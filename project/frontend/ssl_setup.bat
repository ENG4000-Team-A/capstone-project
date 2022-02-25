choco install mkcert
mkcert -install
mkcert localhost
set HTTPS=true&&set SSL_CRT_FILE=localhost.pem&&set SSL_KEY_FILE=localhost-key.pem&&npm start