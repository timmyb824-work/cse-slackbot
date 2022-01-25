#!/bin/bash
cd /home/ec2-user/cse-slackbot
git pull
pm2 restart test.config.js
