# Login + project
oc login --token=<YOUR_TOKEN> --server=<YOUR_OPENSHIFT_API_URL>
$env:PWPGROUP="lostandfound"
oc project "pwp-2026-2-$env:PWPGROUP"

# Secret env file
$SECRET_KEY = -join ((1..64) | ForEach-Object { '{0:x}' -f (Get-Random -Maximum 16) })
@"
SECRET_KEY=$SECRET_KEY
DB_USER=lostandfound
DB_PASS=<PASTE_DB_PASSWORD>
DB_HOST=<PASTE_DB_IP>
DB_NAME=lostandfound-sensorhub
"@ | Set-Content secret.env

oc delete secret lostandfound-secret --ignore-not-found
oc create secret generic lostandfound-secret --from-env-file=secret.env

# Apply deploy + service
oc apply -f templates/Deployment.yaml
oc apply -f templates/Service.yaml

# Route
oc delete route lostandfound --ignore-not-found
oc create route edge lostandfound --service=lostandfound-sensorhub --port=80

# Public URL
$HOST = oc get route lostandfound -o jsonpath='{.spec.host}'
Write-Host "https://$HOST"

# Init DB + test data + master key
$POD = oc get pod -l app=lostandfound-sensorhub -o jsonpath='{.items[0].metadata.name}'
oc exec -it $POD -c sensorhub -- sh -lc 'flask --app=sensorhub init-db && flask --app=sensorhub testgen && flask --app=sensorhub masterkey'

# Verify
curl -H "Sensorhub-Api-Key: <PASTE_KEY>" "https://$HOST/api/sensors/"

# Submission JSON
# {"url":"https://<route-host>","apikey":"<master-key>"}

# Cleanup
oc delete deployment lostandfound-sensorhub --ignore-not-found
oc delete service lostandfound-sensorhub --ignore-not-found
oc delete route lostandfound --ignore-not-found
