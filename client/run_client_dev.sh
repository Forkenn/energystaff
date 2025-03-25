#!/usr/bin/env sh
if [ ! -n "$(ls -A /app/node_modules)" ]; then
  npm install
fi

npm run lint -- --fix ;
npm run dev ;
#rm -rf /app/node_modules/*
#chmod -R 777 /app/node_modules
#mkdir /app/node_modules