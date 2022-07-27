# HLS Data Transfer Dashboard React App

## Prerequisites

1. Node JS
2. NPM


### `Steps to deploy the Dashoboard`

1. Check out source code from github repository()
2. cd into HLS-Transfer-Workflows/Data-Transfer-ReactJS-Dashboard.
3. Execute command **npm install** to install all the dependencies.
4. Execute command **npm run build** to create the build out of source code.
5. Execute command **pm2 serve {path-to-build}/ {port}  --name "{name}"** to deploy the build(e.g : pm2 serve build/ 5000 --name "my-react-app").
