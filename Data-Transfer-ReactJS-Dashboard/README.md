# HLS Data Transfer Dashboard React App

## Prerequisites

1. Node JS (v12.22.9)
2. NPM (v8.5.1)


### `Steps to deploy the Dashboard`

1. Clone or pull source code from github repository(git clone https://github.com/ub0005/HLS-Transfer-Workflows.git or git pull)
2. cd into HLS-Transfer-Workflows/Data-Transfer-ReactJS-Dashboard.
3. Execute command **npm install** to install all the dependencies.
4. Execute command **npm run build** to create the build out of source code.
5. Execute command **npm install pm2 -g** to install pm2 globally
6. Execute command **pm2 serve {path-to-build}/ {port}  --name "{name}"** to deploy the build(e.g : pm2 serve build/ 5000 --name "my-react-app").
