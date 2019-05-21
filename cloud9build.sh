#!/bin/sh
zip -r build/cldawsLambda.zip lambda/*.py
echo "var API_BASE='${CLDAWS_API}';" > build/dspaceLauncher.init.js
aws s3 cp build/cldawsLambda.zip s3://${CLDAWS_BUCKET}
aws s3 cp --acl public-read web/* s3://${CLDAWS_BUCKET}
aws s3 cp --acl public-read build/dspaceLauncher.init.js s3://${CLDAWS_BUCKET}