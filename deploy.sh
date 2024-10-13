#!/bin/bash

# get variables from .env
export $(grep -v '^#' .env | xargs)

# sam build
sam build

# sam deploy
sam deploy \
  --template-file template.yaml \
  --stack-name $APP_NAME \
  --resolve-s3 \
  --parameter-overrides \
    AppName="$APP_NAME" \
    NotionDatabaseId="$NOTION_DATABASE_ID" \
    TelegramToken="$TELEGRAM_TOKEN" \
    NotionToken="$NOTION_TOKEN" \
  --capabilities CAPABILITY_IAM \
  --profile andrii