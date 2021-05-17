cat <<EOF | kubectl apply -f -
---
apiVersion: kubeless.io/v1beta1
kind: Function
metadata:
  name: description-profanity-checker
spec:
  deployment:
    metadata:
      annotations:
        "annotation-to-deploy": "value"
    spec:
      replicas: 2
      template:
        metadata:
          annotations:
            "annotation-to-pod": "value"
  deps: "requirements.txt"
  function: |
    from better_profanity import profanity 
    import json
    def check_for_profanities(event, context):
        print(event['data'])
        loaded_data = json.loads(event['data'])
        print(loaded_data)
        censored_text = {"censoredDescription": profanity.censor(loaded_data['description'])}
        return json.dumps(censored_text)
  function-content-type: text
  handler: description-profanity-checker.check_for_profanities
  runtime: python3.6
  service:
    selector:
      function: description-profanity-checker
    ports:
    - name: http-function-port
      port: 8080
      protocol: TCP
      targetPort: 8080
    type: NodePort
EOF