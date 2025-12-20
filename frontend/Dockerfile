FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy app
COPY . .

# Build production bundle
RUN npm run build

# Serve with a simple HTTP server
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
