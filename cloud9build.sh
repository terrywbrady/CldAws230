#!/bin/sh
rm build/*
cp lambda/*.py build
cd build
zip -r cldawsLambda.zip *.py
cd ..
echo "var API_BASE='${CLDAWS_API}';" > build/dspaceLauncher.init.js

aws s3 cp --acl public-read build/dspaceLauncher.init.js s3://${CLDAWS_BUCKET}

aws s3 cp --acl public-read web/index.html         s3://${CLDAWS_BUCKET}
aws s3 cp --acl public-read web/dspaceLauncher.js  s3://${CLDAWS_BUCKET}
aws s3 cp --acl public-read web/dspaceLauncher.css s3://${CLDAWS_BUCKET}

aws lambda update-function-code --function-name projTestZip        --zip-file fileb://build/cldawsLambda.zip --publish
aws lambda update-function-code --function-name projGetPRs         --zip-file fileb://build/cldawsLambda.zip --publish
aws lambda update-function-code --function-name projListInstances  --zip-file fileb://build/cldawsLambda.zip --publish
aws lambda update-function-code --function-name projStopInstance   --zip-file fileb://build/cldawsLambda.zip --publish
aws lambda update-function-code --function-name projCreateInstance --zip-file fileb://build/cldawsLambda.zip --publish
aws lambda update-function-code --function-name projTimer          --zip-file fileb://build/cldawsLambda.zip --publish