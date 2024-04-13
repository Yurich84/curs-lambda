
### Run localy
`python main.py`

### Deploy
`rm -f code.zip`

`zip code.zip *.py`

`aws lambda update-function-code --function-name curs --zip-file fileb://code.zip`

Or run `deploy.hs`

Do not forget `chmod +x ./deploy.sh`
