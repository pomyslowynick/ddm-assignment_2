curl -L --data '"{\"description\": \"This video is shit!\"}"' --header "Content-Type:application/json" localhost:8080/api/v1/namespaces/default/services/profanity-checker:http-function-port/proxy/
