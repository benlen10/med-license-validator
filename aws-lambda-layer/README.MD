# aws-lambda-layer

## Instructions

    mkdir aws-lambda-layer
    cd aws-lambda-layer
    mkdir -p lambda-layer/python/lib/python3.8/site-packages
    pip3 install requests --target lambda-layer/python/lib/python3.8/site-packages
    pip3 install bs4 --target lambda-layer/python/lib/python3.8/site-packages
    cd lambda-layer
    zip -r9 lambda-layer.zip .
